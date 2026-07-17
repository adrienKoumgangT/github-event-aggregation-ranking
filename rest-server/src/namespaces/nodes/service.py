from typing import Dict, Any, List

from config.logger import get_logger
from namespaces.nodes.models import ClusterNode
from services.yarn_client import YarnClient


logger = get_logger(__name__)


class NodeService:

    @staticmethod
    def get_all_nodes() -> List[ClusterNode]:
        """Get all nodes from the cluster"""
        try:
            result = YarnClient.cluster_nodes()
            if isinstance(result, dict) and 'error' in result:
                logger.error(f"Failed to get nodes: {result.get('error')}")
                return []
            return result if isinstance(result, list) else []
        except Exception as e:
            logger.error(f"Error getting nodes: {e}")
            return []

    @staticmethod
    def get_node(node_id: str) -> ClusterNode | Dict[str, Any]:
        """Get specific node details"""
        try:
            result = YarnClient.cluster_node(node_id)
            if isinstance(result, dict):
                if 'error' in result:
                    logger.error(f"Failed to get node {node_id}: {result.get('error')}")
                return result
            return result
        except Exception as e:
            logger.error(f"Error getting node {node_id}: {e}")
            return {'error': str(e)}

    @staticmethod
    def get_node_statistics() -> Dict[str, Any]:
        """Get node statistics"""
        try:
            nodes = NodeService.get_all_nodes()

            if not nodes:
                return {}

            total_nodes = len(nodes)
            healthy_nodes = len([n for n in nodes if n.state in ['RUNNING', 'NEW']])
            unhealthy_nodes = len([n for n in nodes if n.state not in ['RUNNING', 'NEW']])

            total_memory = sum(n.availMemoryMB + n.usedMemoryMB for n in nodes)
            used_memory = sum(n.usedMemoryMB for n in nodes)
            available_memory = sum(n.availMemoryMB for n in nodes)

            total_vcores = sum(n.availableVirtualCores + n.usedVirtualCores for n in nodes)
            used_vcores = sum(n.usedVirtualCores for n in nodes)
            available_vcores = sum(n.availableVirtualCores for n in nodes)

            total_containers = sum(n.numContainers for n in nodes)

            return {
                'totalNodes': total_nodes,
                'healthyNodes': healthy_nodes,
                'unhealthyNodes': unhealthy_nodes,
                'totalMemoryMB': total_memory,
                'usedMemoryMB': used_memory,
                'availableMemoryMB': available_memory,
                'memoryUtilization': round((used_memory / total_memory * 100) if total_memory > 0 else 0, 2),
                'totalVCores': total_vcores,
                'usedVCores': used_vcores,
                'availableVCores': available_vcores,
                'vCoreUtilization': round((used_vcores / total_vcores * 100) if total_vcores > 0 else 0, 2),
                'totalContainers': total_containers,
                # 'nodes': nodes
            }

        except Exception as e:
            logger.error(f"Error getting node statistics: {e}")
            return {'error': str(e)}

    @staticmethod
    def get_node_resource_utilization(node_id: str) -> Dict[str, Any]:
        """Get resource utilization for a specific node"""
        try:
            node = NodeService.get_node(node_id)

            if not node or isinstance(node, dict):
                return node

            total_memory = node.availMemoryMB + node.usedMemoryMB
            total_vcores = node.availableVirtualCores + node.usedVirtualCores

            return {
                'nodeId': node_id,
                'hostname': node.nodeHostName,
                'state': node.state,
                'memoryUtilization': {
                    'total': total_memory,
                    'used': node.usedMemoryMB,
                    'available': node.availMemoryMB,
                    'percentage': round((node.usedMemoryMB / total_memory * 100) if total_memory > 0 else 0, 2)
                },
                'vCoreUtilization': {
                    'total': total_vcores,
                    'used': node.usedVirtualCores,
                    'available': node.availableVirtualCores,
                    'percentage': round(
                        (node.usedVirtualCores / total_vcores * 100) if total_vcores > 0 else 0, 2)
                },
                'numContainers': node.numContainers,
                'rack': node.rack,
                'version': node.version
            }

        except Exception as e:
            logger.error(f"Error getting node utilization for {node_id}: {e}")
            return {'error': str(e)}

