from flask_restx import fields, Model

job_type_model = Model('JobType', {
    'type': fields.String(description='Job type', enum=['HADOOP', 'SPARK', 'PYTHON']),
    'displayName': fields.String(description='Display name'),
    'description': fields.String(description='Job type description')
})

hadoop_job_model = Model('HadoopJob', {
    'jobName': fields.String(description='Job name'),
    'jarPath': fields.String(description='JAR file path'),
    'mainClass': fields.String(description='Main class'),
    'inputPath': fields.String(description='Input path'),
    'outputPath': fields.String(description='Output path'),
    'arguments': fields.List(fields.String, description='Additional arguments'),
    'memory': fields.Integer(description='Memory in MB', default=1024),
    'vCores': fields.Integer(description='Virtual cores', default=1)
})

spark_job_model = Model('SparkJob', {
    'jobName': fields.String(description='Job name'),
    'scriptPath': fields.String(description='Script path'),
    'inputPath': fields.String(description='Input path'),
    'outputPath': fields.String(description='Output path'),
    'arguments': fields.List(fields.String, description='Additional arguments'),
    'executorMemory': fields.String(description='Executor memory', default='1g'),
    'executorCores': fields.Integer(description='Executor cores', default=1),
    'numExecutors': fields.Integer(description='Number of executors', default=2)
})

python_job_model = Model('PythonJob', {
    'jobName': fields.String(description='Job name'),
    'scriptPath': fields.String(description='Script path'),
    'inputPath': fields.String(description='Input path'),
    'outputPath': fields.String(description='Output path'),
    'arguments': fields.List(fields.String, description='Additional arguments')
})

job_submission_model = Model('JobSubmission', {
    'type': fields.String(description='Job type', enum=['HADOOP', 'SPARK', 'PYTHON']),
    'configuration': fields.Raw(description='Job configuration')
})

job_status_model = Model('JobStatus', {
    'jobId': fields.String(description='Job ID'),
    'applicationId': fields.String(description='Application ID'),
    'type': fields.String(description='Job type'),
    'status': fields.String(description='Job status'),
    'progress': fields.Float(description='Progress'),
    'startTime': fields.Integer(description='Start time'),
    'elapsedTime': fields.Integer(description='Elapsed time')
})

job_result_model = Model('JobResult', {
    'jobId': fields.String(description='Job ID'),
    'status': fields.String(description='Final status'),
    'outputPath': fields.String(description='Output path'),
    'diagnostics': fields.String(description='Diagnostics'),
    'logs': fields.String(description='Job logs')
})
