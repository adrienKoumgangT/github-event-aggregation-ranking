from flask_restx import fields, Model
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
import json


@dataclass
class ClusterNodeResourceUtilization:
    nodePhysicalMemoryMB: int # Node physical memory utilization
    nodeVirtualMemoryMB: int # Node virtual memory utilization
    nodeCPUUsage: float # Node CPU utilization
    aggregatedContainersPhysicalMemoryMB: int # The aggregated physical memory utilization of the containers
    aggregatedContainersVirtualMemoryMB: int # The aggregated virtual memory utilization of the containers
    containersCPUUsage: float # The aggregated CPU utilization of the containers

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ClusterNodeResourceUtilization":
        return cls(
            nodePhysicalMemoryMB=d.get("nodePhysicalMemoryMB", 0),
            nodeVirtualMemoryMB=d.get("nodeVirtualMemoryMB", 0),
            nodeCPUUsage=d.get("nodeCPUUsage", 0.0),
            aggregatedContainersPhysicalMemoryMB=d.get("aggregatedContainersPhysicalMemoryMB", 0),
            aggregatedContainersVirtualMemoryMB=d.get("aggregatedContainersVirtualMemoryMB", 0),
            containersCPUUsage=d.get("containersCPUUsage", 0.0)
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ClusterNodeTotalResource:
    memory: int
    vCores: int

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ClusterNodeTotalResource":
        return cls(
            memory=d.get("memory", 0),
            vCores=d.get("vCores", 0),
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ClusterNode:
    rack: str # The rack location of this node
    state: str # State of the node - valid values are: NEW, RUNNING, UNHEALTHY, DECOMMISSIONING, DECOMMISSIONED, LOST, REBOOTED, SHUTDOWN
    id: str # The node id
    nodeHostName: str # The host name of the node
    nodeHTTPAddress: str # The nodes HTTP address
    lastHealthUpdate: int # The last time the node reported its health (in ms since epoch)
    version: str # Version of hadoop running on node
    healthReport: str # A detailed health report
    numContainers: int # The total number of containers currently running on the node
    usedMemoryMB: int # The total amount of memory currently used on the node (in MB)
    availMemoryMB: int # The total amount of memory currently available on the node (in MB)
    usedVirtualCores: int # The total number of vCores currently used on the node
    availableVirtualCores: int # The total number of vCores available on the node
    resourceUtilization: Optional[ClusterNodeResourceUtilization] = None # Resource utilization on the node
    totalResource: Optional[ClusterNodeTotalResource] = None # Resources on the node

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ClusterNode":
        return cls(
            rack=d.get("rack", ""),
            state=d.get("state", ""),
            id=d.get("id", ""),
            nodeHostName=d.get("nodeHostName", ""),
            nodeHTTPAddress=d.get("nodeHTTPAddress", ""),
            lastHealthUpdate=d.get("lastHealthUpdate", 0),
            version=d.get("version", ""),
            healthReport=d.get("healthReport", ""),
            numContainers=d.get("numContainers", 0),
            usedMemoryMB=d.get("usedMemoryMB", 0),
            availMemoryMB=d.get("availMemoryMB", 0),
            usedVirtualCores=d.get("usedVirtualCores", 0),
            availableVirtualCores=d.get("availableVirtualCores", 0),
            resourceUtilization=ClusterNodeResourceUtilization.from_dict(d.get("resourceUtilization", {})) if d.get("resourceUtilization") else None,
            totalResource=ClusterNodeTotalResource.from_dict(d.get("totalResource", {})) if d.get("totalResource") else None,
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with proper serialization of nested objects"""
        """
        return {
            "rack": self.rack,
            "state": self.state,
            "id": self.id,
            "nodeHostName": self.nodeHostName,
            "nodeHTTPAddress": self.nodeHTTPAddress,
            "lastHealthUpdate": self.lastHealthUpdate,
            "version": self.version,
            "healthReport": self.healthReport,
            "numContainers": self.numContainers,
            "usedMemoryMB": self.usedMemoryMB,
            "availMemoryMB": self.availMemoryMB,
            "usedVirtualCores": self.usedVirtualCores,
            "availableVirtualCores": self.availableVirtualCores,
            "resourceUtilization": self.resourceUtilization.to_dict() if self.resourceUtilization else {},
            "totalResource": self.totalResource.to_dict() if self.totalResource else {},
        }
        """

        result = asdict(self)
        # Remove None and empty values for cleaner output
        return {k: v for k, v in result.items() if v is not None and v != [] and v != {}}


from flask_restx import fields, Model

# Resource Utilization Model
resource_utilization_model = Model('ResourceUtilization', {
    'nodePhysicalMemoryMB': fields.Integer(description='Node physical memory utilization'),
    'nodeVirtualMemoryMB': fields.Integer(description='Node virtual memory utilization'),
    'nodeCPUUsage': fields.Float(description='Node CPU utilization'),
    'aggregatedContainersPhysicalMemoryMB': fields.Integer(description='Aggregated physical memory utilization of containers'),
    'aggregatedContainersVirtualMemoryMB': fields.Integer(description='Aggregated virtual memory utilization of containers'),
    'containersCPUUsage': fields.Float(description='Aggregated CPU utilization of containers')
})

# Total Resource Model
total_resource_model = Model('TotalResource', {
    'memory': fields.Integer(description='Total memory in MB'),
    'vCores': fields.Integer(description='Total virtual cores'),
    'resourceInformations': fields.Raw(description='Additional resource information')
})

# Node Model
node_model = Model('Node', {
    'id': fields.String(description='Node ID'),
    'nodeHostName': fields.String(description='Node hostname'),
    'state': fields.String(description='Node state (NEW, RUNNING, UNHEALTHY, DECOMMISSIONING, DECOMMISSIONED, LOST, REBOOTED, SHUTDOWN)'),
    'nodeHTTPAddress': fields.String(description='Node HTTP address'),
    'healthReport': fields.String(description='Detailed health report'),
    'lastHealthUpdate': fields.Integer(description='Last health update (ms since epoch)'),
    'rack': fields.String(description='Rack name'),
    'numContainers': fields.Integer(description='Number of containers'),
    'usedMemoryMB': fields.Integer(description='Used memory in MB'),
    'availMemoryMB': fields.Integer(description='Available memory in MB'),
    'usedVirtualCores': fields.Integer(description='Used virtual cores'),
    'availableVirtualCores': fields.Integer(description='Available virtual cores'),
    'version': fields.String(description='Hadoop version'),
    'resourceUtilization': fields.Nested(resource_utilization_model, description='Resource utilization'),
    'totalResource': fields.Nested(total_resource_model, description='Total resources on the node')
})


# Node Health Item Model (individual node health)
node_health_item_model = Model('NodeHealthItem', {
    'id': fields.String(description='Node ID'),
    'hostname': fields.String(description='Node hostname'),
    'state': fields.String(description='Node state'),
    'healthStatus': fields.String(description='Derived health status'),
    'lastHealthUpdate': fields.Integer(description='Last health update')
})

# Node Health Model (aggregate health summary)
node_health_model = Model('NodeHealth', {
    'total': fields.Integer(description='Total nodes'),
    'healthy': fields.Integer(description='Healthy nodes'),
    'unhealthy': fields.Integer(description='Unhealthy nodes'),
    'lost': fields.Integer(description='Lost nodes'),
    'decommissioned': fields.Integer(description='Decommissioned nodes'),
    'nodes': fields.List(fields.Nested(node_health_item_model), description='Node health details')
})
