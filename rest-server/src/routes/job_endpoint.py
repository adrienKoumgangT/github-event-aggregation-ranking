from flask import g, jsonify, request
from flask_restx import Namespace, Resource
import logging

logger = logging.getLogger(__name__)

ns_job = Namespace('job', description='Job endpoint')




@ns_job.route('/hadoop')
class JobHadoop(Resource):

    def post(self):
        """Submit a Hadoop MapReduce job"""
        pass


@ns_job.route('/spark')
class JobSpark(Resource):

    def post(self):
        """Submit a spark job"""
        pass


@ns_job.route('/all')
class JobAll(Resource):

    def get(self):
        """Get all jobs status"""
        pass


@ns_job.route('/<job_id>')
class Job(Resource):

    def get(self, job_id):
        """Get status of a specific job"""
        pass

