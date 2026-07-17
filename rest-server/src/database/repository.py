from typing import Optional, List, Dict, Any
from datetime import datetime

from config.logger import get_logger
from database import db
from database.models import Job, JobConfiguration, JobLog, JobStatus, JobType
import uuid


logger = get_logger(__name__)


class JobRepository:
    """Repository for job database operations"""

    @staticmethod
    def create_job(job_data: Dict[str, Any]) -> Job:
        """Create a new job in the database"""
        try:
            job_id = job_data.get('jobId', str(uuid.uuid4()))

            job = Job(
                id=job_id,
                name=job_data.get('name', 'Unnamed Job'),
                type=job_data.get('type', JobType.HADOOP.value),
                status=JobStatus.PENDING.value,
                user=job_data.get('user', 'anonymous'),
                queue=job_data.get('queue', 'default'),
                priority=job_data.get('priority', 0),
                memory_mb=job_data.get('memory', 1024),
                vcores=job_data.get('vCores', 1),
                input_path=job_data.get('inputPath'),
                output_path=job_data.get('outputPath')
            )

            db.session.add(job)
            db.session.flush()  # Flush to get the job ID

            # Create configuration if provided
            config_data = job_data.get('configuration', {})
            if config_data:
                config = JobConfiguration(
                    job_id=job_id,
                    jar_path=config_data.get('jarPath'),
                    main_class=config_data.get('mainClass'),
                    script_path=config_data.get('scriptPath'),
                    executor_memory=config_data.get('executorMemory'),
                    executor_cores=config_data.get('executorCores'),
                    num_executors=config_data.get('numExecutors'),
                    spark_master=config_data.get('sparkMaster'),
                    deploy_mode=config_data.get('deployMode'),
                    python_script_path=config_data.get('pythonScriptPath'),
                    python_executable=config_data.get('pythonExecutable'),
                    arguments=config_data.get('arguments', []),
                    environment_vars=config_data.get('environmentVars', {}),
                    additional_params=config_data.get('additionalParams', {})
                )
                db.session.add(config)

            # Add initial log
            log = JobLog(
                job_id=job_id,
                log_level='INFO',
                message=f'Job created with type {job.type}',
                log_type='SYSTEM'
            )
            db.session.add(log)

            db.session.commit()
            logger.info(f"Job {job_id} created successfully")
            return job

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating job: {e}")
            raise

    @staticmethod
    def get_job(job_id: str) -> Optional[Job]:
        """Get job by ID"""
        return Job.query.get(job_id)

    @staticmethod
    def get_all_jobs(
            status: Optional[str] = None,
            job_type: Optional[str] = None,
            user: Optional[str] = None,
            limit: int = 100,
            offset: int = 0
    ) -> List[Job]:
        """Get all jobs with optional filters"""
        query = Job.query

        if status:
            query = query.filter(Job.status == status)
        if job_type:
            query = query.filter(Job.type == job_type)
        if user:
            query = query.filter(Job.user == user)

        return query.order_by(Job.created_at.desc()).limit(limit).offset(offset).all()

    @staticmethod
    def update_job_status(
            job_id: str,
            status: str,
            progress: Optional[float] = None,
            error_message: Optional[str] = None,
            diagnostics: Optional[str] = None
    ) -> Optional[Job]:
        """Update job status"""
        try:
            job = Job.query.get(job_id)
            if not job:
                return None

            old_status = job.status
            job.status = status

            if progress is not None:
                job.progress = progress

            if error_message:
                job.error_message = error_message

            if diagnostics:
                job.diagnostics = diagnostics

            # Set timestamps based on status
            if status == JobStatus.RUNNING.value and old_status == JobStatus.PENDING.value:
                job.started_at = datetime.utcnow()
            elif status in [JobStatus.FINISHED.value, JobStatus.FAILED.value,
                            JobStatus.KILLED.value, JobStatus.CANCELLED.value]:
                job.finished_at = datetime.utcnow()
                job.final_status = status

            # Add status change log
            log = JobLog(
                job_id=job_id,
                log_level='INFO',
                message=f'Status changed from {old_status} to {status}',
                log_type='SYSTEM'
            )
            db.session.add(log)

            db.session.commit()
            logger.info(f"Job {job_id} status updated to {status}")
            return job

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating job status for {job_id}: {e}")
            raise

    @staticmethod
    def update_job_application_id(job_id: str, application_id: str, application_url: Optional[str] = None) -> Optional[
        Job]:
        """Update job with YARN application ID"""
        try:
            job = Job.query.get(job_id)
            if not job:
                return None

            job.application_id = application_id
            if application_url:
                job.application_url = application_url

            log = JobLog(
                job_id=job_id,
                log_level='INFO',
                message=f'YARN application ID assigned: {application_id}',
                log_type='SYSTEM'
            )
            db.session.add(log)

            db.session.commit()
            logger.info(f"Job {job_id} linked to YARN application {application_id}")
            return job

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating application ID for {job_id}: {e}")
            raise

    @staticmethod
    def add_job_log(
            job_id: str,
            message: str,
            log_level: str = 'INFO',
            log_type: str = 'SYSTEM'
    ) -> Optional[JobLog]:
        """Add a log entry for a job"""
        try:
            job = Job.query.get(job_id)
            if not job:
                return None

            log = JobLog(
                job_id=job_id,
                log_level=log_level,
                message=message,
                log_type=log_type
            )
            db.session.add(log)
            db.session.commit()

            return log

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error adding log for job {job_id}: {e}")
            raise

    @staticmethod
    def get_job_logs(job_id: str, log_level: Optional[str] = None, limit: int = 100) -> List[JobLog]:
        """Get logs for a job"""
        query = JobLog.query.filter(JobLog.job_id == job_id)

        if log_level:
            query = query.filter(JobLog.log_level == log_level)

        return query.order_by(JobLog.timestamp.desc()).limit(limit).all()

    @staticmethod
    def delete_job(job_id: str) -> bool:
        """Delete a job and all related data"""
        try:
            job = Job.query.get(job_id)
            if not job:
                return False

            db.session.delete(job)
            db.session.commit()
            logger.info(f"Job {job_id} deleted")
            return True

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting job {job_id}: {e}")
            raise

    @staticmethod
    def get_job_statistics() -> Dict[str, Any]:
        """Get job statistics"""
        try:
            total_jobs = Job.query.count()
            status_counts = {}

            for status in JobStatus:
                count = Job.query.filter(Job.status == status.value).count()
                if count > 0:
                    status_counts[status.value] = count

            type_counts = {}
            for job_type in JobType:
                count = Job.query.filter(Job.type == job_type.value).count()
                if count > 0:
                    type_counts[job_type.value] = count

            # Recent jobs
            recent_jobs = Job.query.order_by(Job.created_at.desc()).limit(10).all()

            return {
                'totalJobs': total_jobs,
                'statusDistribution': status_counts,
                'typeDistribution': type_counts,
                'recentJobs': [job.to_dict() for job in recent_jobs]
            }

        except Exception as e:
            logger.error(f"Error getting job statistics: {e}")
            raise

