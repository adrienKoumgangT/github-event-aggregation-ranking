from flask_restx import Namespace, Resource
from .models import cluster_info_model, cluster_metrics_model, scheduler_info_model
from .service import ClusterService

cluster_ns = Namespace(
    'cluster',
    description='Cluster information and metrics operations'
)

# Add models to namespace for Swagger
cluster_ns.models[cluster_info_model.name] = cluster_info_model
cluster_ns.models[cluster_metrics_model.name] = cluster_metrics_model
cluster_ns.models[scheduler_info_model.name] = scheduler_info_model

@cluster_ns.route('/info')
class ClusterInfoResource(Resource):

    @cluster_ns.doc('get_cluster_info')
    @cluster_ns.marshal_with(cluster_info_model)
    @cluster_ns.response(200, 'Success')
    @cluster_ns.response(500, 'Internal Server Error')
    def get(self):
        """Get cluster information"""
        return ClusterService.get_cluster_info()

@cluster_ns.route('/metrics')
class ClusterMetricsResource(Resource):

    @cluster_ns.doc('get_cluster_metrics')
    @cluster_ns.marshal_with(cluster_metrics_model)
    @cluster_ns.response(200, 'Success')
    @cluster_ns.response(500, 'Internal Server Error')
    def get(self):
        """Get cluster metrics"""
        return ClusterService.get_cluster_metrics()

@cluster_ns.route('/scheduler')
class ClusterSchedulerResource(Resource):

    @cluster_ns.doc('get_cluster_scheduler')
    @cluster_ns.marshal_with(scheduler_info_model)
    @cluster_ns.response(200, 'Success')
    @cluster_ns.response(500, 'Internal Server Error')
    def get(self):
        """Get scheduler information"""
        return ClusterService.get_scheduler_info()
