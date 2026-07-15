from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List
import json

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

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


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

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)



@dataclass
class ResourceRequestCapability:
    memory: int
    virtualCores: int

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ResourceRequestCapability":
        return cls(
            memory=d.get("memory", 0),
            virtualCores=d.get("virtualCores", 0)
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ResourceRequestPriority:
    priority: int

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ResourceRequestPriority":
        return cls(
            priority=d.get("priority", 0)
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ClusterApplicationResourceRequest:
    capability: ResourceRequestCapability
    nodeLabelExpression: str
    numContainers: int
    priority: ResourceRequestPriority
    relaxLocality: bool
    resourceName: str

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ClusterApplicationResourceRequest":
        return cls(
            capability=ResourceRequestCapability.from_dict(d["capability"]),
            nodeLabelExpression=d.get("nodeLabelExpression", ""),
            numContainers=d.get("numContainers", 0),
            priority=ResourceRequestPriority.from_dict(d["priority"]),
            relaxLocality=d.get("relaxLocality", True),
            resourceName=d.get("resourceName", "")
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ClusterApplicationTimeout:
    type: str
    expiryTime: str
    remainingTimeInSeconds: int

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ClusterApplicationTimeout":
        return cls(
            type=d.get("type", ""),
            expiryTime=d.get("expiryTime", ""),
            remainingTimeInSeconds=d.get("remainingTimeInSeconds", 0)
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ClusterApplication:
    id: str # The application id
    user: str # The user who started the application
    name: str # The application name
    queue: str # The queue the application was submitted to
    state: str # The application state according to the ResourceManager - valid values are members of the YarnApplicationState enum: NEW, NEW_SAVING, SUBMITTED, ACCEPTED, RUNNING, FINISHED, FAILED, KILLED
    finalStatus: str # The final status of the application if finished - reported by the application itself - valid values are the members of the FinalApplicationStatus enum: UNDEFINED, SUCCEEDED, FAILED, KILLED
    progress: float # The progress of the application as a percent
    trackingUI: str # Where the tracking url is currently pointing - History (for history server) or ApplicationMaster
    trackingUrl: str # The web URL that can be used to track the application
    diagnostics: str # Detailed diagnostics information
    clusterId: int # The cluster id
    applicationType: str # The application type
    applicationTags: str # Comma separated tags of an application
    priority: int # Priority of the submitted application
    startedTime: int # The time in which application started (in ms since epoch)
    finishedTime: int # The time in which the application finished (in ms since epoch)
    elapsedTime: int # The elapsed time since the application started (in ms)
    amContainerLogs: str # The URL of the application master container logs
    amHostHttpAddress: str # The nodes http address of the application master
    # amRPCAddress: str # The RPC address of the application master
    allocatedMB: int # The sum of memory in MB allocated to the application’s running containers
    allocatedVCores: int # The sum of virtual cores allocated to the application’s running containers
    runningContainers: int # The number of containers currently running for the application
    memorySeconds: int # The amount of memory the application has allocated (megabyte-seconds)
    vcoreSeconds: int # The amount of CPU resources the application has allocated (virtual core-seconds)
    queueUsagePercentage: float # The percentage of resources of the queue that the app is using
    clusterUsagePercentage: float # The percentage of resources of the cluster that the app is using.
    preemptedResourceMB: int # Memory used by preempted container
    preemptedResourceVCores: int # Number of virtual cores used by preempted container
    numNonAMContainerPreempted: int # Number of standard containers preempted
    numAMContainerPreempted: int # Number of application master containers preempted
    logAggregationStatus: str # Status of log aggregation - valid values are the members of the LogAggregationStatus enum: DISABLED, NOT_START, RUNNING, RUNNING_WITH_FAILURE, SUCCEEDED, FAILED, TIME_OUT
    unmanagedApplication: bool # Is the application unmanaged.
    appNodeLabelExpression: str # Node Label expression which is used to identify the nodes on which application’s containers are expected to run by default.
    amNodeLabelExpression: str # Node Label expression which is used to identify the node on which application’s AM container is expected to run.
    resourceRequests: List[ClusterApplicationResourceRequest]
    timeouts: List[ClusterApplicationTimeout]

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ClusterApplication":
        return cls(
            id=d["id"],
            user=d["user"],
            name=d["name"],
            queue=d["queue"],
            state=d["state"],
            finalStatus=d["finalStatus"],
            progress=d["progress"],
            trackingUI=d["trackingUI"],
            trackingUrl=d["trackingUrl"],
            diagnostics=d["diagnostics"],
            clusterId=d["clusterId"],
            applicationType=d["applicationType"],
            applicationTags=d.get("applicationTags", ""),
            priority=d["priority"],
            startedTime=d["startedTime"],
            finishedTime=d["finishedTime"],
            elapsedTime=d["elapsedTime"],
            amContainerLogs=d["amContainerLogs"],
            amHostHttpAddress=d["amHostHttpAddress"],
            # amRPCAddress=d["amRPCAddress"],
            allocatedMB=d["allocatedMB"],
            allocatedVCores=d["allocatedVCores"],
            runningContainers=d["runningContainers"],
            memorySeconds=d["memorySeconds"],
            vcoreSeconds=d["vcoreSeconds"],
            queueUsagePercentage=d["queueUsagePercentage"],
            clusterUsagePercentage=d["clusterUsagePercentage"],
            preemptedResourceMB=d["preemptedResourceMB"],
            preemptedResourceVCores=d["preemptedResourceVCores"],
            numNonAMContainerPreempted=d["numNonAMContainerPreempted"],
            numAMContainerPreempted=d["numAMContainerPreempted"],
            logAggregationStatus=d["logAggregationStatus"],
            unmanagedApplication=d["unmanagedApplication"],
            appNodeLabelExpression=d.get("appNodeLabelExpression", ""),
            amNodeLabelExpression=d.get("amNodeLabelExpression", ""),
            resourceRequests=[ClusterApplicationResourceRequest.from_dict(req) for req in d.get("resourceRequests", [])],
            timeouts=[ClusterApplicationTimeout.from_dict(t) for t in d.get("timeouts", {}).get("timeout", [])]
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ClusterStatItem:
    state: str
    type: str
    count: int

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ClusterStatItem":
        return cls(
            state=d.get("state", ""),
            type=d.get("type", ""),
            count=d.get("count", 0)
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)



@dataclass
class ClusterAppAttempt:
    id: str # The app attempt id
    nodeId: str # The node id of the node the attempt ran on
    nodeHttpAddress: str # The node http address of the node the attempt ran on
    logsLink: str # The http link to the app attempt logs
    containerId: str # The id of the container for the app attempt
    startTime: int # The start time of the attempt (in ms since epoch)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ClusterAppAttempt":
        return cls(
            id=d.get("id", ""),
            nodeId=d.get("nodeId", ""),
            nodeHttpAddress=d.get("nodeHttpAddress", ""),
            logsLink=d.get("logsLink", ""),
            containerId=d.get("containerId", ""),
            startTime=d.get("startTime", 0)
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class KeyValue:
    key: str
    value: str

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "KeyValue":
        return cls(
            key=d.get("key", ""),
            value=d.get("value", ""),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ClusterAppContainer:
    containerId: str # The container id
    allocatedMB: int # The amount of memory allocated for the container in MB
    allocatedVCores: int # The amount of virtual cores allocated for the container
    assignedNodeId: str # The node id of the node the attempt ran on
    priority: int # Allocated priority of the container
    startedTime: int # The start time of the attempt (in ms since epoch)
    finishedTime: int # The finish time of the attempt (in ms since epoch) 0 if not finished
    elapsedTime: int # The elapsed time in ms since the startedTime
    logUrl: str # The web URL that can be used to check the log for the container
    containerExitStatus: int # Final exit status of the container
    containerState: str # State of the container, can be NEW, RUNNING, or COMPLETE
    nodeHttpAddress: str # The node http address of the node the attempt ran on
    nodeId: str # The node id of the node the attempt ran on
    allocatedResources: List[KeyValue] # Allocated resources for the container: memory (The maximum memory for the container) - vCores (The maximum number of vcores for the container)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ClusterAppContainer":
        return cls(
            containerId=d.get("containerId", ""),
            allocatedMB=d.get("allocatedMB", 0),
            allocatedVCores=d.get("allocatedVCores", 0),
            assignedNodeId=d.get("assignedNodeId", ""),
            priority=d.get("priority", 0),
            startedTime=d.get("startedTime", 0),
            finishedTime=d.get("finishedTime", 0),
            elapsedTime=d.get("elapsedTime", 0),
            logUrl=d.get("logUrl", ""),
            containerExitStatus=d.get("containerExitStatus", 0),
            containerState=d.get("containerState", ""),
            nodeHttpAddress=d.get("nodeHttpAddress", ""),
            nodeId=d.get("nodeId", ""),
            allocatedResources=[KeyValue.from_dict(kv) for kv in d.get("allocatedResources", [])],
        )


@dataclass
class ClusterNodeResourceUtilization:
    nodePhysicalMemoryMB: int # Node physical memory utilization
    nodeVirtualMemoryMB: int # Node virtual memory utilization
    nodeCPUUsage: float# Node CPU utilization
    aggregatedContainersPhysicalMemoryMB: int # The aggregated physical memory utilization of the containers
    aggregatedContainersVirtualMemoryMB: int # The aggregated virtual memory utilization of the containers
    containersCPUUsage: float # The aggregated CPU utilization of the containers

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ClusterNodeResourceUtilization":
        return cls(
            nodePhysicalMemoryMB=d.get("nodePhysicalMemoryMB", 0),
            nodeVirtualMemoryMB=d.get("nodeVirtualMemoryMB", 0),
            nodeCPUUsage=d.get("nodeCPUUsage", 0),
            aggregatedContainersPhysicalMemoryMB=d.get("aggregatedContainersPhysicalMemoryMB", 0),
            aggregatedContainersVirtualMemoryMB=d.get("aggregatedContainersVirtualMemoryMB", 0),
            containersCPUUsage=d.get("containersCPUUsage", 0.0)
        )

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
    resourceUtilization: ClusterNodeResourceUtilization # Resource utilization on the node
    totalResource: ClusterNodeTotalResource # Resources on the node

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
            resourceUtilization=ClusterNodeResourceUtilization.from_dict(d.get("resourceUtilization", {})),
            totalResource=ClusterNodeTotalResource.from_dict(d.get("totalResource", {})),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ClusterNewApplication:
    application_id: str
    maximum_resource_capability: ClusterNodeTotalResource

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ClusterNewApplication":
        return cls(
            application_id=d.get("application-id", ""),
            maximum_resource_capability=ClusterNodeTotalResource.from_dict(d.get("maximum-resource-capability", {})),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# --- app submit ---


@dataclass
class LocalResourceEntry:
    resource: str  # Location of the resource to be localized
    type: str  # Type of the resource; options are "ARCHIVE", "FILE", and "PATTERN"
    visibility: str  # Visibility the resource to be localized; options are "PUBLIC", "PRIVATE", and "APPLICATION"
    size: int  # Size of the resource to be localized
    timestamp: int  # Timestamp of the resource to be localized


@dataclass
class Credentials:
    tokens: Optional[Dict[str, str]] = field(default_factory=dict)  # Tokens as key-value pairs
    secrets: Optional[Dict[str, str]] = field(default_factory=dict)  # Secrets as key-value pairs (base-64 encoded)


@dataclass
class Resource:
    memory: int  # Memory required for each container
    vCores: int  # Virtual cores required for each container


@dataclass
class LogAggregationContext:
    log_include_pattern: Optional[str] = None  # Log files matching this pattern will be uploaded
    log_exclude_pattern: Optional[str] = None  # Log files matching this pattern will not be uploaded
    rolled_log_include_pattern: Optional[str] = None  # Log files matching this pattern will be aggregated in rolling fashion
    rolled_log_exclude_pattern: Optional[str] = None  # Log files matching this pattern will not be aggregated in rolling fashion
    log_aggregation_policy_class_name: Optional[str] = None  # Policy class for log aggregation
    log_aggregation_policy_parameters: Optional[str] = None  # Parameters passed to the policy class


@dataclass
class AMBlackListingRequests:
    am_black_listing_enabled: bool = False  # Whether AM Blacklisting is enabled
    disable_failure_threshold: float = 0.0  # AM Blacklisting disable failure threshold


@dataclass
class AMContainerSpec:
    local_resources: Optional[Dict[str, LocalResourceEntry]] = field(default_factory=dict)  # Resources that need to be localized
    environment: Optional[Dict[str, str]] = field(default_factory=dict)  # Environment variables for containers
    commands: Optional[List[str]] = field(default_factory=list)  # Commands for launching containers
    service_data: Optional[Dict[str, str]] = field(default_factory=dict)  # Application specific service data (base-64 encoded)
    credentials: Optional[Credentials] = None  # Credentials required for application
    application_acls: Optional[Dict[str, str]] = field(default_factory=dict)  # ACLs for application (VIEW_APP, MODIFY_APP)


@dataclass
class ClusterAppSubmit:
    application_id: str  # The application id
    application_name: str  # The application name
    queue: Optional[str] = None  # The name of the queue
    priority: int = 0  # The priority of the application
    am_container_spec: AMContainerSpec = field(default_factory=AMContainerSpec)  # The application master container launch context
    unmanaged_am: bool = False  # Is the application using an unmanaged application master
    max_app_attempts: int = 1  # The max number of attempts for this application
    resource: Resource = field(default_factory=lambda: Resource(memory=1024, vCores=1))  # The resources the application master requires
    application_type: str = "YARN"  # The application type (MapReduce, Pig, Hive, etc)
    keep_containers_across_application_attempts: bool = False  # Keep containers across application attempts
    application_tags: Optional[List[str]] = field(default_factory=list)  # List of application tags
    log_aggregation_context: Optional[LogAggregationContext] = None  # Log aggregation information
    attempt_failures_validity_interval: Optional[int] = None  # Failure validity interval
    reservation_id: Optional[str] = None  # Unique id of reserved resource allocation
    am_black_listing_requests: Optional[AMBlackListingRequests] = None  # AM blacklisting information

    def to_json(self) -> str:
        """Convert the object to JSON format for the API request."""
        return json.dumps(self.to_dict(), indent=2)

    def to_dict(self) -> dict:
        """Convert the object to a dictionary matching the API JSON format."""
        result = {
            "application-id": self.application_id,
            "application-name": self.application_name,
            "priority": self.priority,
            "am-container-spec": {},
            "unmanaged-AM": self.unmanaged_am,
            "max-app-attempts": self.max_app_attempts,
            "resource": {
                "memory": self.resource.memory,
                "vCores": self.resource.vCores
            },
            "application-type": self.application_type,
            "keep-containers-across-application-attempts": self.keep_containers_across_application_attempts
        }

        if self.queue:
            result["queue"] = self.queue

        # Build am-container-spec
        am_spec = self.am_container_spec
        if am_spec.local_resources:
            result["am-container-spec"]["local-resources"] = {
                "entry": [
                    {
                        "key": key,
                        "value": {
                            "resource": val.resource,
                            "type": val.type,
                            "visibility": val.visibility,
                            "size": val.size,
                            "timestamp": val.timestamp
                        }
                    }
                    for key, val in am_spec.local_resources.items()
                ]
            }

        if am_spec.environment:
            result["am-container-spec"]["environment"] = {
                "entry": [
                    {"key": key, "value": value}
                    for key, value in am_spec.environment.items()
                ]
            }

        if am_spec.commands:
            result["am-container-spec"]["commands"] = {
                "command": am_spec.commands[0] if len(am_spec.commands) == 1 else " && ".join(am_spec.commands)
            }

        if am_spec.service_data:
            result["am-container-spec"]["service-data"] = {
                "entry": [
                    {"key": key, "value": value}
                    for key, value in am_spec.service_data.items()
                ]
            }

        if am_spec.credentials:
            creds = {}
            if am_spec.credentials.tokens:
                creds["tokens"] = am_spec.credentials.tokens
            if am_spec.credentials.secrets:
                creds["secrets"] = {
                    "entry": [
                        {"key": key, "value": value}
                        for key, value in am_spec.credentials.secrets.items()
                    ]
                }
            if creds:
                result["am-container-spec"]["credentials"] = creds

        if am_spec.application_acls:
            result["am-container-spec"]["application-acls"] = {
                "entry": [
                    {"key": key, "value": value}
                    for key, value in am_spec.application_acls.items()
                ]
            }

        # Optional fields
        if self.application_tags:
            result["application-tags"] = {"tag": self.application_tags}

        if self.log_aggregation_context:
            log_ctx = self.log_aggregation_context
            result["log-aggregation-context"] = {}
            if log_ctx.log_include_pattern:
                result["log-aggregation-context"]["log-include-pattern"] = log_ctx.log_include_pattern
            if log_ctx.log_exclude_pattern:
                result["log-aggregation-context"]["log-exclude-pattern"] = log_ctx.log_exclude_pattern
            if log_ctx.rolled_log_include_pattern:
                result["log-aggregation-context"]["rolled-log-include-pattern"] = log_ctx.rolled_log_include_pattern
            if log_ctx.rolled_log_exclude_pattern:
                result["log-aggregation-context"]["rolled-log-exclude-pattern"] = log_ctx.rolled_log_exclude_pattern
            if log_ctx.log_aggregation_policy_class_name:
                result["log-aggregation-context"]["log-aggregation-policy-class-name"] = log_ctx.log_aggregation_policy_class_name
            if log_ctx.log_aggregation_policy_parameters:
                result["log-aggregation-context"]["log-aggregation-policy-parameters"] = log_ctx.log_aggregation_policy_parameters

        if self.attempt_failures_validity_interval is not None:
            result["attempt-failures-validity-interval"] = self.attempt_failures_validity_interval

        if self.reservation_id:
            result["reservation-id"] = self.reservation_id

        if self.am_black_listing_requests:
            result["am-black-listing-requests"] = {
                "am-black-listing-enabled": self.am_black_listing_requests.am_black_listing_enabled,
                "disable-failure-threshold": self.am_black_listing_requests.disable_failure_threshold
            }

        return result