from services.yarn_client import YarnClient


class ClusterService:

    @staticmethod
    def get_cluster_info():
        """Get cluster information from YARN"""
        return YarnClient.cluster_info()

    @staticmethod
    def get_cluster_metrics():
        """Get cluster metrics from YARN"""
        return YarnClient.cluster_metrics()

    @staticmethod
    def get_scheduler_info():
        """Get scheduler information from YARN"""
        return YarnClient.cluster_scheduler()
