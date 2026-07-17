from flask_restx import fields, Model
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List
import json


# Cluster Info Models

@dataclass
class ClusterInfo:
    id: int # The cluster id
    startedOn: int # The time the cluster started (in ms since epoch)
    state: str # The ResourceManager state - valid values are: NOTINITED, INITED, STARTED, STOPPED
    haState: str # The ResourceManager HA state - valid values are: INITIALIZING, ACTIVE, STANDBY, STOPPED
    rmStateStoreName: str # Fully qualified name of class that implements the storage of ResourceManager state
    resourceManagerVersion: str # Version of the ResourceManager
    resourceManagerBuildVersion: str # ResourceManager build string with build version, user, and checksum
    resourceManagerVersionBuiltOn: str # Timestamp when ResourceManager was built (in ms since epoch)
    hadoopVersion: str # Version of hadoop common
    hadoopBuildVersion: str # Hadoop common build string with build version, user, and checksum
    hadoopVersionBuiltOn: str # Timestamp when hadoop common was built(in ms since epoch)
    haZooKeeperConnectionState: str # State of ZooKeeper connection of the high availability service


    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ClusterInfo":
        return cls(
            id=d["id"],
            startedOn=d["startedOn"],
            state=d["state"],
            haState=d["haState"],
            rmStateStoreName=d["rmStateStoreName"],
            resourceManagerVersion=d["resourceManagerVersion"],
            resourceManagerBuildVersion=d["resourceManagerBuildVersion"],
            resourceManagerVersionBuiltOn=d["resourceManagerVersionBuiltOn"],
            hadoopVersion=d["hadoopVersion"],
            hadoopBuildVersion=d["hadoopBuildVersion"],
            hadoopVersionBuiltOn=d["hadoopVersionBuiltOn"],
            haZooKeeperConnectionState=d["haZooKeeperConnectionState"],
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

cluster_info_model = Model('ClusterInfo', {
    'id': fields.Integer(description='Cluster ID'),
    'startedOn': fields.Integer(description='Cluster start time'),
    'state': fields.String(description='Cluster state'),
    'hadoopVersion': fields.String(description='Hadoop version'),
    'resourceManagerVersion': fields.String(description='Resource Manager version')
})


# Cluster Metrics Models

@dataclass
class ClusterMetrics:
    appsSubmitted: int # The number of applications submitted
    appsCompleted: int # The number of applications completed
    appsPending: int # The number of applications pending
    appsRunning: int # The number of applications running
    appsFailed: int # The number of applications failed
    appsKilled: int # The number of applications killed
    reservedMB: int # The amount of memory reserved in MB
    availableMB: int # The amount of memory available in MB
    allocatedMB: int # The amount of memory allocated in MB
    totalMB: int # The amount of total memory in MB
    reservedVirtualCores: int # The number of reserved virtual cores
    availableVirtualCores: int # The number of available virtual cores
    allocatedVirtualCores: int # The number of allocated virtual cores
    totalVirtualCores: int # The total number of virtual cores
    containersAllocated: int # The number of containers allocated
    containersReserved: int # The number of containers reserved
    containersPending: int # The number of containers pending
    totalNodes: int # The total number of nodes
    activeNodes: int # The number of active nodes
    lostNodes: int # The number of lost nodes
    unhealthyNodes: int # The number of unhealthy nodes
    decommissioningNodes: int # The number of nodes being decommissioned
    decommissionedNodes: int # The number of nodes decommissioned
    rebootedNodes: int # The number of nodes rebooted
    shutdownNodes: int # The number of nodes shut down

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ClusterMetrics":
        return cls(
            appsSubmitted=d["appsSubmitted"],
            appsCompleted=d["appsCompleted"],
            appsPending=d["appsPending"],
            appsRunning=d["appsRunning"],
            appsFailed=d["appsFailed"],
            appsKilled=d["appsKilled"],
            reservedMB=d["reservedMB"],
            availableMB=d["availableMB"],
            allocatedMB=d["allocatedMB"],
            totalMB=d["totalMB"],
            reservedVirtualCores=d["reservedVirtualCores"],
            availableVirtualCores=d["availableVirtualCores"],
            allocatedVirtualCores=d["allocatedVirtualCores"],
            totalVirtualCores=d["totalVirtualCores"],
            containersAllocated=d["containersAllocated"],
            containersReserved=d["containersReserved"],
            containersPending=d["containersPending"],
            totalNodes=d["totalNodes"],
            activeNodes=d["activeNodes"],
            lostNodes=d["lostNodes"],
            unhealthyNodes=d["unhealthyNodes"],
            decommissioningNodes=d["decommissioningNodes"],
            decommissionedNodes=d["decommissionedNodes"],
            rebootedNodes=d["rebootedNodes"],
            shutdownNodes=d["shutdownNodes"],
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

cluster_metrics_model = Model('ClusterMetrics', {
    'appsSubmitted': fields.Integer(description='Number of submitted apps'),
    'appsCompleted': fields.Integer(description='Number of completed apps'),
    'appsPending': fields.Integer(description='Number of pending apps'),
    'appsRunning': fields.Integer(description='Number of running apps'),
    'appsFailed': fields.Integer(description='Number of failed apps'),
    'appsKilled': fields.Integer(description='Number of killed apps'),
    'availableMB': fields.Integer(description='Available memory in MB'),
    'allocatedMB': fields.Integer(description='Allocated memory in MB'),
    'availableVirtualCores': fields.Integer(description='Available virtual cores'),
    'allocatedVirtualCores': fields.Integer(description='Allocated virtual cores'),
    'containersAllocated': fields.Integer(description='Number of allocated containers'),
    'containersReserved': fields.Integer(description='Number of reserved containers'),
    'containersPending': fields.Integer(description='Number of pending containers'),
    'totalMB': fields.Integer(description='Total memory in MB'),
    'totalVirtualCores': fields.Integer(description='Total virtual cores'),
    'totalNodes': fields.Integer(description='Total number of nodes'),
    'lostNodes': fields.Integer(description='Number of lost nodes'),
    'unhealthyNodes': fields.Integer(description='Number of unhealthy nodes'),
    'decommissionedNodes': fields.Integer(description='Number of decommissioned nodes'),
    'rebootedNodes': fields.Integer(description='Number of rebooted nodes'),
    'activeNodes': fields.Integer(description='Number of active nodes')
})



# Scheduler Info Model
scheduler_info_model = Model('SchedulerInfo', {
    'type': fields.String(description='Scheduler type'),
    'capacity': fields.Raw(description='Scheduler capacity info'),
    'queues': fields.Raw(description='Queue information')
})

