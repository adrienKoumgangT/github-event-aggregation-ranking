import json
import requests
import time
from typing import Dict, Any, List, Optional
import uuid
import os

from config.logger import get_logger
from config.settings import Config
from namespaces.applications.models import AMContainerSpec, Resource, ClusterAppSubmit
from services.yarn_client import YarnClient
from database.repository import JobRepository
from database.models import Job, JobStatus, JobType


logger = get_logger(__name__)


class JobService:

    @staticmethod
    def get_job_types() -> List[Dict[str, Any]]:
        """Get available job types"""
        return [
            {
                'type': JobType.HADOOP.value,
                'displayName': 'Hadoop MapReduce',
                'description': 'Run Hadoop MapReduce jobs using JAR files',
                'parameters': [
                    {'name': 'jarPath', 'label': 'JAR Path', 'type': 'text', 'required': True,
                     'description': 'Path to the JAR file'},
                    {'name': 'mainClass', 'label': 'Main Class', 'type': 'text', 'required': True,
                     'description': 'Main class (e.g., it.unipi.App)'},
                    {'name': 'topN', 'label': 'Top N', 'type': 'number', 'required': False, 'default': 10,
                     'description': 'Number of top results'},
                    {'name': 'inputPath', 'label': 'Input Path', 'type': 'text', 'required': True,
                     'description': 'HDFS input path'},
                    {'name': 'intermediatePath', 'label': 'Intermediate Path', 'type': 'text', 'required': False,
                     'description': 'HDFS intermediate path (auto-generated if empty)'},
                    {'name': 'outputPath', 'label': 'Final Output Path', 'type': 'text', 'required': True,
                     'description': 'HDFS final output path'},
                    {'name': 'arguments', 'label': 'Additional Arguments', 'type': 'array', 'required': False,
                     'description': 'Extra command line arguments'},
                    {'name': 'memory', 'label': 'Memory (MB)', 'type': 'number', 'required': False, 'default': 1024},
                    {'name': 'vCores', 'label': 'Virtual Cores', 'type': 'number', 'required': False, 'default': 1}
                ]
            },
            {
                'type': JobType.SPARK.value,
                'displayName': 'Apache Spark',
                'description': 'Run Spark jobs using Python scripts',
                'parameters': [
                    {'name': 'scriptPath', 'label': 'Script Path', 'type': 'text', 'required': True},
                    {'name': 'inputPath', 'label': 'Input Path', 'type': 'text', 'required': True},
                    {'name': 'outputPath', 'label': 'Output Path', 'type': 'text', 'required': True},
                    {'name': 'arguments', 'label': 'Arguments', 'type': 'array', 'required': False},
                    {'name': 'executorMemory', 'label': 'Executor Memory', 'type': 'text', 'required': False,
                     'default': '1g'},
                    {'name': 'executorCores', 'label': 'Executor Cores', 'type': 'number', 'required': False,
                     'default': 1},
                    {'name': 'numExecutors', 'label': 'Number of Executors', 'type': 'number', 'required': False,
                     'default': 2}
                ]
            },
            {
                'type': JobType.PYTHON.value,
                'displayName': 'Python Script',
                'description': 'Run standalone Python scripts',
                'parameters': [
                    {'name': 'scriptPath', 'label': 'Script Path', 'type': 'text', 'required': True},
                    {'name': 'inputPath', 'label': 'Input Path', 'type': 'text', 'required': True},
                    {'name': 'outputPath', 'label': 'Output Path', 'type': 'text', 'required': True},
                    {'name': 'arguments', 'label': 'Arguments', 'type': 'array', 'required': False}
                ]
            }
        ]

    @staticmethod
    def submit_job(data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a new job via YARN REST API"""
        try:
            job_type = data.get('type')
            configuration = data.get('configuration', {})

            if not job_type:
                return {'error': 'Job type is required', 'status_code': 400}

            # Create job in database
            job_id = data.get('jobId', str(uuid.uuid4()))

            if job_type == JobType.HADOOP.value and not configuration.get('intermediatePath'):
                configuration['intermediatePath'] = f"{Config.HADOOP_OUTPUT_DIR}/{job_id}_intermediate"

            if 'memory' not in configuration:
                if job_type == JobType.HADOOP.value:
                    configuration['memory'] = 1024  # Safe default for your cluster
                elif job_type == JobType.SPARK.value:
                    configuration['memory'] = 1024
                else:
                    configuration['memory'] = 1024

            job_data = {
                'jobId': job_id,
                'name': configuration.get('jobName', f'{job_type}_job_{job_id[:8]}'),
                'type': job_type,
                'user': data.get('user', 'anonymous'),
                'queue': data.get('queue', 'default'),
                'priority': data.get('priority', 0),
                'memory': configuration.get('memory', 1024),
                'vCores': configuration.get('vCores', 1),
                'inputPath': configuration.get('inputPath'),
                'outputPath': configuration.get('outputPath'),
                'configuration': configuration
            }

            # Save to database
            job = JobRepository.create_job(job_data)
            JobRepository.add_job_log(job_id, f'Job submitted as {job_type}', 'INFO', 'SYSTEM')

            # Submit via YARN REST API based on type
            if job_type == JobType.HADOOP.value:
                result = JobService._submit_hadoop_via_yarn(job, configuration)
            elif job_type == JobType.SPARK.value:
                result = JobService._submit_spark_via_yarn(job, configuration)
            elif job_type == JobType.PYTHON.value:
                result = JobService._submit_python_via_yarn(job, configuration)
            else:
                JobRepository.update_job_status(job_id, JobStatus.FAILED.value,
                                                error_message=f'Unsupported job type: {job_type}')
                return {'error': f'Unsupported job type: {job_type}', 'status_code': 400}

            # Update job status based on result
            if result.get('status') == 'SUBMITTED':
                JobRepository.update_job_status(job_id, JobStatus.RUNNING.value)

                if result.get('applicationId'):
                    JobRepository.update_job_application_id(
                        job_id,
                        result['applicationId'],
                        result.get('applicationUrl')
                    )

                JobRepository.add_job_log(job_id, 'Job submitted successfully via YARN', 'INFO', 'SYSTEM')
            else:
                JobRepository.update_job_status(
                    job_id,
                    JobStatus.FAILED.value,
                    error_message=result.get('error', 'Failed to submit job')
                )

            return {
                'jobId': job_id,
                'status': result.get('status', 'FAILED'),
                'message': 'Job submitted successfully' if result.get(
                    'status') == 'SUBMITTED' else 'Job submission failed',
                'applicationId': result.get('applicationId')
            }

        except Exception as e:
            logger.error(f"Error submitting job: {e}")
            return {'error': str(e), 'status_code': 500}

    @staticmethod
    def _get_cluster_max_resources() -> Dict[str, int]:
        """Get maximum resource capabilities from the cluster"""
        try:
            new_app = YarnClient.cluster_new_application()
            if hasattr(new_app, 'maximum_resource_capability'):
                max_res = new_app.maximum_resource_capability
                return {
                    'memory': getattr(max_res, 'memory', 1536),
                    'vCores': getattr(max_res, 'vCores', 4)
                }
        except Exception as e:
            logger.warning(f"Failed to get cluster max resources: {e}")

        return {'memory': 1536, 'vCores': 4}

    @staticmethod
    def _submit_hadoop_via_yarn(job: Job, config: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a Hadoop MapReduce job via YARN REST API"""
        try:
            job_id = job.id

            jar_path = config.get('jarPath', Config.HADOOP_JAR_PATH)
            main_class = config.get('mainClass', Config.HADOOP_MAIN_CLASS)
            input_path = config.get('inputPath', Config.HADOOP_INPUT_DIR)
            output_path = config.get('outputPath', f"{Config.HADOOP_OUTPUT_DIR}/{job_id}")
            top_n = config.get('topN', 10)
            intermediate_path = config.get('intermediatePath', f"{Config.HADOOP_OUTPUT_DIR}/{job_id}_intermediate")

            # Build the command
            hadoop_command = (
                f"{{HADOOP_HOME}}/bin/hadoop jar "
                f"{jar_path} "
                f"{main_class} "
                f"{top_n} "
                f"{input_path} "
                f"{intermediate_path} "
                f"{output_path}"
            )

            if config.get('arguments'):
                hadoop_command += " " + " ".join(config['arguments'])

            logger.info(f"Hadoop command: {hadoop_command}")
            JobRepository.add_job_log(job_id, f'Command: {hadoop_command}', 'INFO', 'APPLICATION')

            # Get new application ID (includes cluster max resource info)
            new_app = YarnClient.cluster_new_application()
            if isinstance(new_app, dict) and 'error' in new_app:
                raise Exception(f"Failed to get new application ID: {new_app.get('error')}")

            application_id = new_app.application_id if hasattr(new_app, 'application_id') else new_app.get('application-id')

            # Get max resource capabilities from the response
            max_memory = 1536
            max_vcores = 4

            if hasattr(new_app, 'maximum_resource_capability'):
                max_res = new_app.maximum_resource_capability
                if hasattr(max_res, 'memory'):
                    max_memory = max_res.memory
                if hasattr(max_res, 'vCores'):
                    max_vcores = max_res.vCores

            # Use requested memory but cap at cluster maximum
            requested_memory = min(int(config.get('memory', 1024)), max_memory)
            requested_vcores = min(int(config.get('vCores', 1)), max_vcores)

            logger.info(f"Cluster max - Memory: {max_memory}MB, vCores: {max_vcores}")
            logger.info(f"Requesting - Memory: {requested_memory}MB, vCores: {requested_vcores}")

            # Build request body
            request_body = {
                "application-id": application_id,
                "application-name": f"hadoop_{job_id[:8]}",
                "queue": job.queue or "default",
                "priority": job.priority or 0,
                "am-container-spec": {
                    "commands": {
                        "command": hadoop_command
                    },
                    "environment": {
                        "entry": [
                            {"key": "HADOOP_HOME", "value": Config.HADOOP_HOME},
                            {"key": "HADOOP_CONF_DIR", "value": Config.HADOOP_CONF_DIR},
                            {"key": "JAVA_HOME", "value": "/usr/lib/jvm/java-8-openjdk"}
                        ]
                    }
                },
                "unmanaged-AM": False,
                "max-app-attempts": 2,
                "resource": {
                    "memory": requested_memory,
                    "vCores": requested_vcores
                },
                "application-type": "MAPREDUCE",
                "keep-containers-across-application-attempts": False,
                "application-tags": {
                    "tag": ["hadoop", "mapreduce"]
                }
            }

            # Submit to YARN
            url = f"{YarnClient.rm_url}/apps"

            logger.info(f"Submitting to YARN: {json.dumps(request_body, indent=2)}")

            response = requests.post(url, json=request_body)

            if response.status_code == 202:
                JobRepository.add_job_log(
                    job_id,
                    f'Submitted to YARN. App ID: {application_id}',
                    'INFO',
                    'SYSTEM'
                )
                return {
                    'status': 'SUBMITTED',
                    'applicationId': application_id,
                    'applicationUrl': response.headers.get('Location'),
                    'command': hadoop_command
                }
            else:
                error_msg = response.text
                logger.error(f"YARN submission failed: {error_msg}")
                return {'status': 'FAILED', 'error': error_msg}

        except Exception as e:
            logger.error(f"Error submitting Hadoop job via YARN: {e}")
            return {'status': 'FAILED', 'error': str(e)}

    @staticmethod
    def _submit_spark_via_yarn(job: Job, config: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a Spark job via YARN REST API"""
        try:
            job_id = job.id

            spark_command = (
                f"{{SPARK_HOME}}/bin/spark-submit "
                f"--master yarn "
                f"--deploy-mode cluster "
                f"--executor-memory {config.get('executorMemory', '1g')} "
                f"--executor-cores {config.get('executorCores', 1)} "
                f"--num-executors {config.get('numExecutors', 2)} "
                f"--name spark_job_{job_id[:8]} "
                f"{config.get('scriptPath', Config.SPARK_SCRIPT)} "
                f"--input {config.get('inputPath', Config.HADOOP_INPUT_DIR)} "
                f"--output {config.get('outputPath', f'{Config.HADOOP_OUTPUT_DIR}/{job_id}')}"
            )

            if config.get('arguments'):
                spark_command += " " + " ".join(config['arguments'])

            logger.info(f"Spark command: {spark_command}")
            JobRepository.add_job_log(job_id, f'Command: {spark_command}', 'INFO', 'APPLICATION')

            new_app = YarnClient.cluster_new_application()
            if isinstance(new_app, dict) and 'error' in new_app:
                raise Exception(f"Failed to get new application ID: {new_app.get('error')}")

            application_id = new_app.application_id if hasattr(new_app, 'application_id') else new_app.get(
                'application-id')

            request_body = {
                "application-id": application_id,
                "application-name": f"spark_{job_id[:8]}",
                "queue": job.queue or "default",
                "priority": job.priority or 0,
                "am-container-spec": {
                    "commands": {
                        "command": spark_command
                    },
                    "environment": {
                        "entry": [
                            {"key": "SPARK_HOME", "value": Config.SPARK_HOME},
                            {"key": "HADOOP_CONF_DIR", "value": Config.HADOOP_CONF_DIR}
                        ]
                    }
                },
                "unmanaged-AM": False,
                "max-app-attempts": 2,
                "resource": {
                    "memory": config.get('memory', 2048),
                    "vCores": config.get('vCores', 2)
                },
                "application-type": "SPARK",
                "keep-containers-across-application-attempts": False,
                "application-tags": {
                    "tag": ["spark"]
                }
            }

            url = f"{YarnClient.rm_url}/apps"
            response = requests.post(url, json=request_body)

            if response.status_code == 202:
                JobRepository.add_job_log(job_id, f'Submitted to YARN. App ID: {application_id}', 'INFO', 'SYSTEM')
                return {
                    'status': 'SUBMITTED',
                    'applicationId': application_id,
                    'applicationUrl': response.headers.get('Location'),
                    'command': spark_command
                }
            else:
                return {'status': 'FAILED', 'error': response.text}

        except Exception as e:
            logger.error(f"Error submitting Spark job via YARN: {e}")
            return {'status': 'FAILED', 'error': str(e)}

    @staticmethod
    def _submit_python_via_yarn(job: Job, config: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a Python job via YARN REST API"""
        try:
            job_id = job.id

            python_command = (
                f"python3 "
                f"{config.get('scriptPath', Config.PYTHON_NON_PARALLEL_SCRIPT)} "
                f"--input {config.get('inputPath', Config.HADOOP_INPUT_DIR)} "
                f"--output {config.get('outputPath', f'{Config.HADOOP_OUTPUT_DIR}/{job_id}')}"
            )

            if config.get('arguments'):
                python_command += " " + " ".join(config['arguments'])

            logger.info(f"Python command: {python_command}")
            JobRepository.add_job_log(job_id, f'Command: {python_command}', 'INFO', 'APPLICATION')

            new_app = YarnClient.cluster_new_application()
            if isinstance(new_app, dict) and 'error' in new_app:
                raise Exception(f"Failed to get new application ID: {new_app.get('error')}")

            application_id = new_app.application_id if hasattr(new_app, 'application_id') else new_app.get(
                'application-id')

            request_body = {
                "application-id": application_id,
                "application-name": f"python_{job_id[:8]}",
                "queue": job.queue or "default",
                "priority": job.priority or 0,
                "am-container-spec": {
                    "commands": {
                        "command": python_command
                    },
                    "environment": {
                        "entry": [
                            {"key": "PYTHONPATH", "value": "/usr/local/lib/python3"},
                            {"key": "HADOOP_CONF_DIR", "value": Config.HADOOP_CONF_DIR}
                        ]
                    }
                },
                "unmanaged-AM": False,
                "max-app-attempts": 1,
                "resource": {
                    "memory": 512,
                    "vCores": 1
                },
                "application-type": "YARN",
                "keep-containers-across-application-attempts": False
            }

            url = f"{YarnClient.rm_url}/apps"
            response = requests.post(url, json=request_body)

            if response.status_code == 202:
                JobRepository.add_job_log(job_id, f'Submitted to YARN. App ID: {application_id}', 'INFO', 'SYSTEM')
                return {
                    'status': 'SUBMITTED',
                    'applicationId': application_id,
                    'applicationUrl': response.headers.get('Location'),
                    'command': python_command
                }
            else:
                return {'status': 'FAILED', 'error': response.text}

        except Exception as e:
            logger.error(f"Error submitting Python job via YARN: {e}")
            return {'status': 'FAILED', 'error': str(e)}

    @staticmethod
    def get_job_status(job_id: str) -> Dict[str, Any]:
        """Get job status from database and YARN"""
        try:
            # Get from database
            job = JobRepository.get_job(job_id)
            if not job:
                return {'error': 'Job not found', 'status_code': 404}

            # Check YARN status if available
            if job.application_id and job.status == JobStatus.RUNNING.value:
                try:
                    # Get application state from YARN
                    app_state = YarnClient.get_application_state(job.application_id)
                    if app_state.get('status_code') == 200:
                        yarn_state = app_state.get('state')

                        # Update progress from YARN
                        app_result = YarnClient.cluster_app(job.application_id)
                        if app_result and not isinstance(app_result, dict):
                            progress = getattr(app_result, 'progress', 0)
                            JobRepository.update_job_status(job_id, job.status, progress=progress)

                        # Map YARN states to job states
                        state_mapping = {
                            'FINISHED': JobStatus.FINISHED.value,
                            'FAILED': JobStatus.FAILED.value,
                            'KILLED': JobStatus.KILLED.value
                        }
                        if yarn_state in state_mapping:
                            JobRepository.update_job_status(job_id, state_mapping[yarn_state])
                            JobRepository.add_job_log(
                                job_id,
                                f'Job {yarn_state.lower()} (YARN state)',
                                'INFO',
                                'SYSTEM'
                            )
                except Exception as e:
                    logger.warning(f"Failed to check YARN status for {job.application_id}: {e}")

            return job.to_dict(include_config=True)

        except Exception as e:
            logger.error(f"Error getting job status {job_id}: {e}")
            return {'error': str(e), 'status_code': 500}

    @staticmethod
    def get_all_jobs(
            status: Optional[str] = None,
            job_type: Optional[str] = None,
            user: Optional[str] = None,
            limit: int = 100,
            offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Get all jobs with filters"""
        try:
            jobs = JobRepository.get_all_jobs(status, job_type, user, limit, offset)
            return [job.to_dict() for job in jobs]
        except Exception as e:
            logger.error(f"Error getting all jobs: {e}")
            return []

    @staticmethod
    def get_job_result(job_id: str) -> Dict[str, Any]:
        """Get job results"""
        try:
            job = JobRepository.get_job(job_id)
            if not job:
                return {'error': 'Job not found', 'status_code': 404}

            # Get logs
            logs = JobRepository.get_job_logs(job_id)

            # If job has YARN application ID, get additional info
            diagnostics = job.diagnostics or ''
            if job.application_id:
                try:
                    app_result = YarnClient.cluster_app(job.application_id)
                    if app_result and not isinstance(app_result, dict):
                        diagnostics = getattr(app_result, 'diagnostics', '')
                except Exception as e:
                    logger.warning(f"Failed to get YARN app info: {e}")

            return {
                'jobId': job_id,
                'status': job.status,
                'finalStatus': job.final_status,
                'outputPath': job.output_path,
                'diagnostics': diagnostics,
                'errorMessage': job.error_message,
                'logs': [log.to_dict() for log in logs]
            }

        except Exception as e:
            logger.error(f"Error getting job result {job_id}: {e}")
            return {'error': str(e), 'status_code': 500}

    @staticmethod
    def kill_job(job_id: str) -> Dict[str, Any]:
        """Kill a running job"""
        try:
            job = JobRepository.get_job(job_id)
            if not job:
                return {'error': 'Job not found', 'status_code': 404}

            # Kill YARN application if exists
            if job.application_id:
                try:
                    kill_result = YarnClient.kill_application(job.application_id)
                    if kill_result.get('status_code') in [200, 202]:
                        JobRepository.add_job_log(job_id, 'Killed YARN application', 'INFO', 'SYSTEM')
                    else:
                        logger.warning(f"Kill may have failed: {kill_result}")
                except Exception as e:
                    logger.warning(f"Failed to kill YARN app {job.application_id}: {e}")

            JobRepository.update_job_status(job_id, JobStatus.KILLED.value, progress=100.0)
            JobRepository.add_job_log(job_id, 'Job killed', 'INFO', 'SYSTEM')

            return {
                'jobId': job_id,
                'status': JobStatus.KILLED.value,
                'message': 'Job killed successfully'
            }

        except Exception as e:
            logger.error(f"Error killing job {job_id}: {e}")
            return {'error': str(e), 'status_code': 500}

    @staticmethod
    def get_job_logs(job_id: str, log_level: Optional[str] = None) -> Dict[str, Any]:
        """Get job logs"""
        try:
            job = JobRepository.get_job(job_id)
            if not job:
                return {'error': 'Job not found', 'status_code': 404}

            logs = JobRepository.get_job_logs(job_id, log_level)

            return {
                'jobId': job_id,
                'logs': [log.to_dict() for log in logs],
                'status': job.status
            }

        except Exception as e:
            logger.error(f"Error getting job logs {job_id}: {e}")
            return {'error': str(e), 'status_code': 500}

    @staticmethod
    def get_job_statistics() -> Dict[str, Any]:
        """Get job statistics"""
        try:
            return JobRepository.get_job_statistics()
        except Exception as e:
            logger.error(f"Error getting job statistics: {e}")
            return {'error': str(e)}

    @staticmethod
    def delete_job(job_id: str) -> Dict[str, Any]:
        """Delete a job"""
        try:
            # Kill first if running
            job = JobRepository.get_job(job_id)
            if job and job.status == JobStatus.RUNNING.value:
                JobService.kill_job(job_id)

            success = JobRepository.delete_job(job_id)
            if success:
                return {'message': 'Job deleted successfully', 'status_code': 200}
            else:
                return {'error': 'Job not found', 'status_code': 404}

        except Exception as e:
            logger.error(f"Error deleting job {job_id}: {e}")
            return {'error': str(e), 'status_code': 500}
