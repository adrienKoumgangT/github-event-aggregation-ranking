from typing import Dict, Any, List, Optional
import uuid
import os
import subprocess

from config.logger import get_logger
from config.settings import Config
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
                    {'name': 'jarPath', 'label': 'JAR Path', 'type': 'text', 'required': True},
                    {'name': 'mainClass', 'label': 'Main Class', 'type': 'text', 'required': True},
                    {'name': 'inputPath', 'label': 'Input Path', 'type': 'text', 'required': True},
                    {'name': 'outputPath', 'label': 'Output Path', 'type': 'text', 'required': True},
                    {'name': 'arguments', 'label': 'Arguments', 'type': 'array', 'required': False},
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
        """Submit a new job"""
        try:
            job_type = data.get('type')
            configuration = data.get('configuration', {})

            if not job_type:
                return {'error': 'Job type is required', 'status_code': 400}

            # Create job in database
            job_id = data.get('jobId', str(uuid.uuid4()))
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

            # Submit based on type
            if job_type == JobType.HADOOP.value:
                result = JobService._submit_hadoop_job(job, configuration)
            elif job_type == JobType.SPARK.value:
                result = JobService._submit_spark_job(job, configuration)
            elif job_type == JobType.PYTHON.value:
                result = JobService._submit_python_job(job, configuration)
            else:
                JobRepository.update_job_status(job_id, JobStatus.FAILED.value,
                                                error_message=f'Unsupported job type: {job_type}')
                return {'error': f'Unsupported job type: {job_type}', 'status_code': 400}

            # Update job status based on result
            if result.get('status') == 'SUBMITTED':
                JobRepository.update_job_status(job_id, JobStatus.RUNNING.value)

                # Store application ID if available
                if result.get('applicationId'):
                    JobRepository.update_job_application_id(
                        job_id,
                        result['applicationId'],
                        result.get('applicationUrl')
                    )

                JobRepository.add_job_log(job_id, 'Job started successfully', 'INFO', 'SYSTEM')
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
    def _submit_hadoop_job(job: Job, config: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a Hadoop MapReduce job"""
        try:
            job_id = job.id
            output_path = config.get('outputPath', f"{Config.HADOOP_OUTPUT_DIR}/{job_id}")

            # Build the Hadoop command
            hadoop_cmd = [
                os.path.join(Config.HADOOP_HOME, 'bin', 'hadoop'),
                'jar',
                config.get('jarPath', Config.HADOOP_JAR_PATH),
                config.get('mainClass', Config.HADOOP_MAIN_CLASS),
                config.get('inputPath', Config.HADOOP_INPUT_DIR),
                output_path
            ]

            # Add additional arguments
            if config.get('arguments'):
                hadoop_cmd.extend(config['arguments'])

            # Log the command
            command_str = ' '.join(hadoop_cmd)
            logger.info(f"Executing Hadoop command: {command_str}")
            JobRepository.add_job_log(job_id, f'Executing: {command_str}', 'INFO', 'APPLICATION')

            # Execute the command asynchronously
            process = subprocess.Popen(
                hadoop_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Store process for monitoring
            JobService._store_process(job_id, process)

            return {
                'status': 'SUBMITTED',
                'applicationId': f'hadoop_{job_id}',
                'command': command_str
            }

        except Exception as e:
            logger.error(f"Error submitting Hadoop job: {e}")
            return {'status': 'FAILED', 'error': str(e)}

    @staticmethod
    def _submit_spark_job(job: Job, config: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a Spark job"""
        try:
            job_id = job.id
            output_path = config.get('outputPath', f"{Config.HADOOP_OUTPUT_DIR}/{job_id}")

            # Build the Spark submit command
            spark_cmd = [
                os.path.join(Config.SPARK_HOME, 'bin', 'spark-submit'),
                '--master', config.get('sparkMaster', 'yarn'),
                '--deploy-mode', config.get('deployMode', 'cluster'),
                '--executor-memory', config.get('executorMemory', '1g'),
                '--executor-cores', str(config.get('executorCores', 1)),
                '--num-executors', str(config.get('numExecutors', 2)),
                '--name', f'spark_job_{job_id}',
                config.get('scriptPath', Config.SPARK_SCRIPT),
                '--input', config.get('inputPath', Config.HADOOP_INPUT_DIR),
                '--output', output_path
            ]

            # Add additional arguments
            if config.get('arguments'):
                spark_cmd.extend(config['arguments'])

            # Log the command
            command_str = ' '.join(spark_cmd)
            logger.info(f"Executing Spark command: {command_str}")
            JobRepository.add_job_log(job_id, f'Executing: {command_str}', 'INFO', 'APPLICATION')

            # Execute the command
            process = subprocess.Popen(
                spark_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Store process for monitoring
            JobService._store_process(job_id, process)

            return {
                'status': 'SUBMITTED',
                'applicationId': f'spark_{job_id}',
                'command': command_str
            }

        except Exception as e:
            logger.error(f"Error submitting Spark job: {e}")
            return {'status': 'FAILED', 'error': str(e)}

    @staticmethod
    def _submit_python_job(job: Job, config: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a Python job"""
        try:
            job_id = job.id
            output_path = config.get('outputPath', f"{Config.HADOOP_OUTPUT_DIR}/{job_id}")

            # Build the Python command
            python_cmd = [
                config.get('pythonExecutable', 'python3'),
                config.get('scriptPath', Config.PYTHON_NON_PARALLEL_SCRIPT),
                '--input', config.get('inputPath', Config.HADOOP_INPUT_DIR),
                '--output', output_path
            ]

            # Add additional arguments
            if config.get('arguments'):
                python_cmd.extend(config['arguments'])

            # Log the command
            command_str = ' '.join(python_cmd)
            logger.info(f"Executing Python command: {command_str}")
            JobRepository.add_job_log(job_id, f'Executing: {command_str}', 'INFO', 'APPLICATION')

            # Execute the command
            process = subprocess.Popen(
                python_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Store process for monitoring
            JobService._store_process(job_id, process)

            return {
                'status': 'SUBMITTED',
                'applicationId': f'python_{job_id}',
                'command': command_str
            }

        except Exception as e:
            logger.error(f"Error submitting Python job: {e}")
            return {'status': 'FAILED', 'error': str(e)}

    # Process tracking
    _processes = {}

    @classmethod
    def _store_process(cls, job_id: str, process: subprocess.Popen):
        """Store a subprocess for monitoring"""
        cls._processes[job_id] = process

    @classmethod
    def _check_process(cls, job_id: str) -> Optional[Dict[str, Any]]:
        """Check the status of a subprocess"""
        if job_id in cls._processes:
            process = cls._processes[job_id]
            poll = process.poll()

            if poll is not None:
                # Process has finished
                stdout, stderr = process.communicate()

                if poll == 0:
                    JobRepository.update_job_status(job_id, JobStatus.FINISHED.value, progress=100.0)
                    JobRepository.add_job_log(job_id, 'Job completed successfully', 'INFO', 'SYSTEM')
                else:
                    JobRepository.update_job_status(
                        job_id,
                        JobStatus.FAILED.value,
                        progress=100.0,
                        error_message=stderr[:500]
                    )
                    JobRepository.add_job_log(job_id, f'Job failed with exit code {poll}', 'ERROR', 'SYSTEM')

                # Store output as logs
                if stdout:
                    JobRepository.add_job_log(job_id, f'STDOUT:\n{stdout[:1000]}', 'INFO', 'APPLICATION')
                if stderr:
                    JobRepository.add_job_log(job_id, f'STDERR:\n{stderr[:1000]}', 'ERROR', 'APPLICATION')

                del cls._processes[job_id]
                return {'status': 'FINISHED' if poll == 0 else 'FAILED'}

        return None

    @staticmethod
    def get_job_status(job_id: str) -> Dict[str, Any]:
        """Get job status from database"""
        try:
            # Check process first
            JobService._check_process(job_id)

            # Get from database
            job = JobRepository.get_job(job_id)
            if not job:
                return {'error': 'Job not found', 'status_code': 404}

            # Check YARN status if available
            if job.application_id and job.status == JobStatus.RUNNING.value:
                try:
                    app_result = YarnClient.get_application_state(job.application_id)
                    if app_result.get('status_code') == 200:
                        yarn_state = app_result.get('state')
                        # Map YARN states to job states
                        state_mapping = {
                            'FINISHED': JobStatus.FINISHED.value,
                            'FAILED': JobStatus.FAILED.value,
                            'KILLED': JobStatus.KILLED.value
                        }
                        if yarn_state in state_mapping:
                            JobRepository.update_job_status(job_id, state_mapping[yarn_state])
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
            JobService._check_process(job_id)

            job = JobRepository.get_job(job_id)
            if not job:
                return {'error': 'Job not found', 'status_code': 404}

            # Get logs
            logs = JobRepository.get_job_logs(job_id)

            return {
                'jobId': job_id,
                'status': job.status,
                'finalStatus': job.final_status,
                'outputPath': job.output_path,
                'diagnostics': job.diagnostics,
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
                    YarnClient.kill_application(job.application_id)
                    JobRepository.add_job_log(job_id, 'Killed YARN application', 'INFO', 'SYSTEM')
                except Exception as e:
                    logger.warning(f"Failed to kill YARN app {job.application_id}: {e}")

            # Kill process if exists
            if job_id in JobService._processes:
                process = JobService._processes[job_id]
                process.kill()
                del JobService._processes[job_id]
                JobRepository.add_job_log(job_id, 'Killed process', 'INFO', 'SYSTEM')

            JobRepository.update_job_status(job_id, JobStatus.KILLED.value, progress=100.0)

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
