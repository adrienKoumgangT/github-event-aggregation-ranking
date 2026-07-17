from datetime import datetime
from enum import Enum
from database import db
from sqlalchemy.dialects.sqlite import JSON


class JobStatus(str, Enum):
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    FINISHED = 'FINISHED'
    FAILED = 'FAILED'
    KILLED = 'KILLED'
    CANCELLED = 'CANCELLED'


class JobType(str, Enum):
    HADOOP = 'HADOOP'
    SPARK = 'SPARK'
    PYTHON = 'PYTHON'


class Job(db.Model):
    """Main job table"""
    __tablename__ = 'jobs'

    id = db.Column(db.String(36), primary_key=True)  # UUID
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # HADOOP, SPARK, PYTHON
    status = db.Column(db.String(50), nullable=False, default=JobStatus.PENDING.value)
    progress = db.Column(db.Float, default=0.0)

    # YARN specific
    application_id = db.Column(db.String(255), nullable=True)
    application_url = db.Column(db.String(500), nullable=True)

    # Timing
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime, nullable=True)
    finished_at = db.Column(db.DateTime, nullable=True)

    # User info
    user = db.Column(db.String(100), nullable=True)
    queue = db.Column(db.String(100), nullable=True)

    # Job details
    priority = db.Column(db.Integer, default=0)
    memory_mb = db.Column(db.Integer, default=1024)
    vcores = db.Column(db.Integer, default=1)

    # Paths
    input_path = db.Column(db.String(500), nullable=True)
    output_path = db.Column(db.String(500), nullable=True)

    # Results
    final_status = db.Column(db.String(50), nullable=True)
    diagnostics = db.Column(db.Text, nullable=True)
    error_message = db.Column(db.Text, nullable=True)

    # Relationships
    configuration = db.relationship('JobConfiguration', backref='job', uselist=False, cascade='all, delete-orphan')
    logs = db.relationship('JobLog', backref='job', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self, include_logs=False, include_config=True):
        """Convert job to dictionary"""
        result = {
            'jobId': self.id,
            'name': self.name,
            'type': self.type,
            'status': self.status,
            'progress': self.progress,
            'applicationId': self.application_id,
            'applicationUrl': self.application_url,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'startedAt': self.started_at.isoformat() if self.started_at else None,
            'finishedAt': self.finished_at.isoformat() if self.finished_at else None,
            'user': self.user,
            'queue': self.queue,
            'priority': self.priority,
            'memoryMB': self.memory_mb,
            'vCores': self.vcores,
            'inputPath': self.input_path,
            'outputPath': self.output_path,
            'finalStatus': self.final_status,
            'diagnostics': self.diagnostics,
            'errorMessage': self.error_message,
            'elapsedTime': self._calculate_elapsed_time()
        }

        if include_config and self.configuration:
            result['configuration'] = self.configuration.to_dict()

        if include_logs:
            result['logs'] = [log.to_dict() for log in self.logs.all()]

        return result

    def _calculate_elapsed_time(self):
        """Calculate elapsed time in seconds"""
        if self.started_at:
            end_time = self.finished_at if self.finished_at else datetime.utcnow()
            return int((end_time - self.started_at).total_seconds())
        return 0

    def __repr__(self):
        return f'<Job {self.id}: {self.name} ({self.status})>'


class JobConfiguration(db.Model):
    """Job configuration details"""
    __tablename__ = 'job_configurations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.String(36), db.ForeignKey('jobs.id'), nullable=False)

    # Hadoop specific
    jar_path = db.Column(db.String(500), nullable=True)
    main_class = db.Column(db.String(255), nullable=True)

    # Spark specific
    script_path = db.Column(db.String(500), nullable=True)
    executor_memory = db.Column(db.String(50), nullable=True)
    executor_cores = db.Column(db.Integer, nullable=True)
    num_executors = db.Column(db.Integer, nullable=True)
    spark_master = db.Column(db.String(100), nullable=True)
    deploy_mode = db.Column(db.String(50), nullable=True)

    # Python specific
    python_script_path = db.Column(db.String(500), nullable=True)
    python_executable = db.Column(db.String(100), nullable=True)

    # Common
    arguments = db.Column(JSON, nullable=True)  # Store as JSON array
    environment_vars = db.Column(JSON, nullable=True)
    additional_params = db.Column(JSON, nullable=True)  # Any extra parameters

    def to_dict(self):
        """Convert configuration to dictionary"""
        return {
            'jarPath': self.jar_path,
            'mainClass': self.main_class,
            'scriptPath': self.script_path,
            'executorMemory': self.executor_memory,
            'executorCores': self.executor_cores,
            'numExecutors': self.num_executors,
            'sparkMaster': self.spark_master,
            'deployMode': self.deploy_mode,
            'pythonScriptPath': self.python_script_path,
            'pythonExecutable': self.python_executable,
            'arguments': self.arguments or [],
            'environmentVars': self.environment_vars or {},
            'additionalParams': self.additional_params or {}
        }

    def __repr__(self):
        return f'<JobConfiguration for job {self.job_id}>'


class JobLog(db.Model):
    """Job logs"""
    __tablename__ = 'job_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.String(36), db.ForeignKey('jobs.id'), nullable=False)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    log_level = db.Column(db.String(20), default='INFO')  # INFO, WARN, ERROR, DEBUG
    message = db.Column(db.Text, nullable=False)
    log_type = db.Column(db.String(50), default='SYSTEM')  # SYSTEM, APPLICATION, USER

    def to_dict(self):
        """Convert log to dictionary"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'level': self.log_level,
            'message': self.message,
            'type': self.log_type
        }

    def __repr__(self):
        return f'<JobLog {self.id}: {self.log_level} - {self.message[:50]}>'

