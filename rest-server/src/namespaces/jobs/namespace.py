from flask_restx import Namespace, Resource, reqparse
from .models import (
    job_type_model, hadoop_job_model, spark_job_model,
    python_job_model, job_submission_model, job_status_model,
    job_result_model
)
from .service import JobService

jobs_ns = Namespace(
    'jobs',
    description='Job submission and management operations'
)

# Register models
for model in [job_type_model, hadoop_job_model, spark_job_model,
              python_job_model, job_submission_model, job_status_model,
              job_result_model]:
    jobs_ns.models[model.name] = model

# Parser for filtering and pagination
job_filter_parser = reqparse.RequestParser()
job_filter_parser.add_argument('status', type=str,
                               help='Filter by job status (PENDING, RUNNING, FINISHED, FAILED, KILLED)')
job_filter_parser.add_argument('type', type=str, help='Filter by job type (HADOOP, SPARK, PYTHON)')
job_filter_parser.add_argument('user', type=str, help='Filter by user')
job_filter_parser.add_argument('limit', type=int, default=100, help='Number of jobs to return (default: 100)')
job_filter_parser.add_argument('offset', type=int, default=0, help='Offset for pagination (default: 0)')


@jobs_ns.route('/')
class JobListResource(Resource):

    @jobs_ns.doc('list_jobs')
    @jobs_ns.expect(job_filter_parser)
    @jobs_ns.marshal_list_with(job_status_model)
    @jobs_ns.response(200, 'Success')
    @jobs_ns.response(500, 'Internal Server Error')
    def get(self):
        """Get all jobs with optional filters and pagination"""
        args = job_filter_parser.parse_args()

        return JobService.get_all_jobs(
            status=args.get('status'),
            job_type=args.get('type'),
            user=args.get('user'),
            limit=args.get('limit', 100),
            offset=args.get('offset', 0)
        )


@jobs_ns.route('/statistics')
class JobStatisticsResource(Resource):

    @jobs_ns.doc('get_job_statistics')
    @jobs_ns.response(200, 'Success')
    @jobs_ns.response(500, 'Internal Server Error')
    def get(self):
        """Get job statistics"""
        return JobService.get_job_statistics()


@jobs_ns.route('/types')
class JobTypesResource(Resource):

    @jobs_ns.doc('get_job_types')
    @jobs_ns.marshal_list_with(job_type_model)
    def get(self):
        """Get available job types"""
        return JobService.get_job_types()


@jobs_ns.route('/submit')
class JobSubmitResource(Resource):

    @jobs_ns.doc('submit_job')
    @jobs_ns.expect(job_submission_model)
    @jobs_ns.response(202, 'Job submitted')
    @jobs_ns.response(400, 'Invalid request')
    def post(self):
        """Submit a new job"""
        return JobService.submit_job(jobs_ns.payload)


@jobs_ns.route('/<string:job_id>')
@jobs_ns.param('job_id', 'The job identifier')
class JobDetailResource(Resource):

    @jobs_ns.doc('get_job_status')
    @jobs_ns.marshal_with(job_status_model)
    def get(self, job_id):
        """Get job status"""
        return JobService.get_job_status(job_id)


@jobs_ns.route('/<string:job_id>/result')
@jobs_ns.param('job_id', 'The job identifier')
class JobResultResource(Resource):

    @jobs_ns.doc('get_job_result')
    @jobs_ns.marshal_with(job_result_model)
    def get(self, job_id):
        """Get job results"""
        return JobService.get_job_result(job_id)


@jobs_ns.route('/<string:job_id>/kill')
@jobs_ns.param('job_id', 'The job identifier')
class JobKillResource(Resource):

    @jobs_ns.doc('kill_job')
    def put(self, job_id):
        """Kill a running job"""
        return JobService.kill_job(job_id)


@jobs_ns.route('/<string:job_id>/logs')
@jobs_ns.param('job_id', 'The job identifier')
class JobLogsResource(Resource):

    @jobs_ns.doc('get_job_logs')
    def get(self, job_id):
        """Get job logs"""
        return JobService.get_job_logs(job_id)


@jobs_ns.route('/<string:job_id>')
@jobs_ns.param('job_id', 'The job identifier')
class JobDeleteResource(Resource):

    @jobs_ns.doc('delete_job')
    @jobs_ns.response(200, 'Job deleted')
    @jobs_ns.response(404, 'Job not found')
    def delete(self, job_id):
        """Delete a job"""
        return JobService.delete_job(job_id)


