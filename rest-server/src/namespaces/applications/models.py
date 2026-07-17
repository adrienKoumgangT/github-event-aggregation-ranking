from enum import Enum
from flask_restx import fields, Model
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List, Optional
import json

from namespaces.nodes.models import ClusterNodeTotalResource


# Application Models

@dataclass
class ResourceInformation:
    name: str
    value: int
    units: str
    resourceType: str
    minimumAllocation: int
    maximumAllocation: int

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ResourceInformation":
        return cls(
            name=d.get("name", ""),
            value=d.get("value", 0),
            units=d.get("units", ""),
            resourceType=d.get("resourceType", ""),
            minimumAllocation=d.get("minimumAllocation", 0),
            maximumAllocation=d.get("maximumAllocation", 0)
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ResourceInformations:
    resourceInformation: List[ResourceInformation] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ResourceInformations":
        return cls(
            resourceInformation=[
                ResourceInformation.from_dict(ri)
                for ri in d.get("resourceInformation", [])
            ]
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ResourceRequestCapability:
    memory: int
    vCores: int
    resourceInformations: Optional[ResourceInformations] = None

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ResourceRequestCapability":
        return cls(
            memory=d.get("memory", 0),
            vCores=d.get("vCores", 0),
            resourceInformations=ResourceInformations.from_dict(d.get("resourceInformations", {})) if d.get("resourceInformations") else None
        )

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ExecutionTypeRequest:
    executionType: str
    enforceExecutionType: bool

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ExecutionTypeRequest":
        return cls(
            executionType=d.get("executionType", "GUARANTEED"),
            enforceExecutionType=d.get("enforceExecutionType", False)
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ResourceRequest:
    capability: ResourceRequestCapability
    nodeLabelExpression: str
    numContainers: int
    priority: int
    relaxLocality: bool
    resourceName: str
    executionTypeRequest: Optional[ExecutionTypeRequest] = None
    enforceExecutionType: bool = False

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ResourceRequest":
        return cls(
            capability=ResourceRequestCapability.from_dict(d.get("capability", {})),
            nodeLabelExpression=d.get("nodeLabelExpression", ""),
            numContainers=d.get("numContainers", 0),
            priority=d.get("priority", 0),
            relaxLocality=d.get("relaxLocality", True),
            resourceName=d.get("resourceName", ""),
            executionTypeRequest=ExecutionTypeRequest.from_dict(d.get("executionTypeRequest", {})) if d.get("executionTypeRequest") else None,
            enforceExecutionType=d.get("enforceExecutionType", False)
        )

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        return {k: v for k, v in result.items() if v is not None and v != [] and v != {}}


@dataclass
class ResourceUsage:
    memory: int
    vCores: int
    resourceInformations: Optional[ResourceInformations] = None

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ResourceUsage":
        return cls(
            memory=d.get("memory", 0),
            vCores=d.get("vCores", 0),
            resourceInformations=ResourceInformations.from_dict(d.get("resourceInformations", {})) if d.get("resourceInformations") else None
        )

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ResourceUsagesByPartition:
    partitionName: str
    used: ResourceUsage
    reserved: ResourceUsage
    pending: ResourceUsage
    amUsed: Optional[ResourceUsage] = None
    amLimit: Optional[ResourceUsage] = None
    userAmLimit: Optional[ResourceUsage] = None

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ResourceUsagesByPartition":
        return cls(
            partitionName=d.get("partitionName", ""),
            used=ResourceUsage.from_dict(d.get("used", {})),
            reserved=ResourceUsage.from_dict(d.get("reserved", {})),
            pending=ResourceUsage.from_dict(d.get("pending", {})),
            amUsed=ResourceUsage.from_dict(d.get("amUsed", {})) if d.get("amUsed") else None,
            amLimit=ResourceUsage.from_dict(d.get("amLimit", {})) if d.get("amLimit") else None,
            userAmLimit=ResourceUsage.from_dict(d.get("userAmLimit", {})) if d.get("userAmLimit") else None
        )

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ResourceInfo:
    resourceUsagesByPartition: List[ResourceUsagesByPartition] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ResourceInfo":
        return cls(
            resourceUsagesByPartition=[
                ResourceUsagesByPartition.from_dict(partition)
                for partition in d.get("resourceUsagesByPartition", [])
            ]
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ApplicationTimeout:
    type: str
    expiryTime: str
    remainingTimeInSeconds: int

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ApplicationTimeout":
        return cls(
            type=d.get("type", ""),
            expiryTime=d.get("expiryTime", ""),
            remainingTimeInSeconds=d.get("remainingTimeInSeconds", -1)
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ResourceSecondsMapEntry:
    key: str
    value: str

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ResourceSecondsMapEntry":
        return cls(
            key=d.get("key", ""),
            value=d.get("value", "")
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Application:
    id: str
    user: str
    name: str
    queue: str
    state: str
    finalStatus: str
    progress: float
    trackingUI: str
    trackingUrl: str
    diagnostics: str
    clusterId: int
    applicationType: str
    applicationTags: str
    priority: int
    startedTime: int
    launchTime: int
    finishedTime: int
    elapsedTime: int
    amContainerLogs: str
    amHostHttpAddress: str
    amRPCAddress: str
    masterNodeId: str
    allocatedMB: int
    allocatedVCores: int
    reservedMB: int
    reservedVCores: int
    runningContainers: int
    memorySeconds: int
    vcoreSeconds: int
    queueUsagePercentage: float
    clusterUsagePercentage: float
    preemptedResourceMB: int
    preemptedResourceVCores: int
    numNonAMContainerPreempted: int
    numAMContainerPreempted: int
    preemptedMemorySeconds: int
    preemptedVcoreSeconds: int
    logAggregationStatus: str
    unmanagedApplication: bool
    amNodeLabelExpression: str
    resourceRequests: List[ResourceRequest] = field(default_factory=list)
    resourceInfo: Optional[ResourceInfo] = None
    timeouts: List[ApplicationTimeout] = field(default_factory=list)
    resourceSecondsMap: List[ResourceSecondsMapEntry] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Application":
        # Handle resourceSecondsMap which can be a list of entries
        resource_seconds_map = []
        rs_map = d.get("resourceSecondsMap", {})
        if isinstance(rs_map, dict):
            entries = rs_map.get("entry", [])
            if isinstance(entries, dict):
                entries = [entries]
            resource_seconds_map = [
                ResourceSecondsMapEntry.from_dict(entry) for entry in entries
            ]

        return cls(
            id=d.get("id", ""),
            user=d.get("user", ""),
            name=d.get("name", ""),
            queue=d.get("queue", ""),
            state=d.get("state", ""),
            finalStatus=d.get("finalStatus", "UNDEFINED"),
            progress=float(d.get("progress", 0.0)),
            trackingUI=d.get("trackingUI", ""),
            trackingUrl=d.get("trackingUrl", ""),
            diagnostics=d.get("diagnostics", ""),
            clusterId=d.get("clusterId", 0),
            applicationType=d.get("applicationType", ""),
            applicationTags=d.get("applicationTags", ""),
            priority=d.get("priority", 0),
            startedTime=d.get("startedTime", 0),
            launchTime=d.get("launchTime", 0),
            finishedTime=d.get("finishedTime", 0),
            elapsedTime=d.get("elapsedTime", 0),
            amContainerLogs=d.get("amContainerLogs", ""),
            amHostHttpAddress=d.get("amHostHttpAddress", ""),
            amRPCAddress=d.get("amRPCAddress", ""),
            masterNodeId=d.get("masterNodeId", ""),
            allocatedMB=d.get("allocatedMB", 0),
            allocatedVCores=d.get("allocatedVCores", 0),
            reservedMB=d.get("reservedMB", 0),
            reservedVCores=d.get("reservedVCores", 0),
            runningContainers=d.get("runningContainers", 0),
            memorySeconds=d.get("memorySeconds", 0),
            vcoreSeconds=d.get("vcoreSeconds", 0),
            queueUsagePercentage=float(d.get("queueUsagePercentage", 0.0)),
            clusterUsagePercentage=float(d.get("clusterUsagePercentage", 0.0)),
            preemptedResourceMB=d.get("preemptedResourceMB", 0),
            preemptedResourceVCores=d.get("preemptedResourceVCores", 0),
            numNonAMContainerPreempted=d.get("numNonAMContainerPreempted", 0),
            numAMContainerPreempted=d.get("numAMContainerPreempted", 0),
            preemptedMemorySeconds=d.get("preemptedMemorySeconds", 0),
            preemptedVcoreSeconds=d.get("preemptedVcoreSeconds", 0),
            logAggregationStatus=d.get("logAggregationStatus", "DISABLED"),
            unmanagedApplication=d.get("unmanagedApplication", False),
            amNodeLabelExpression=d.get("amNodeLabelExpression", ""),
            resourceRequests=[
                ResourceRequest.from_dict(req)
                for req in d.get("resourceRequests", [])
            ],
            resourceInfo=ResourceInfo.from_dict(d.get("resourceInfo", {})) if d.get("resourceInfo") else None,
            timeouts=[
                ApplicationTimeout.from_dict(t)
                for t in d.get("timeouts", {}).get("timeout", [])
            ],
            resourceSecondsMap=resource_seconds_map
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        # Remove None and empty values for cleaner output
        return {k: v for k, v in result.items() if v is not None and v != [] and v != {}}


@dataclass
class StatItem:
    state: str
    type: str
    count: int

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "StatItem":
        return cls(
            state=d.get("state", ""),
            type=d.get("type", ""),
            count=d.get("count", 0)
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)



@dataclass
class AppAttempt:
    id: str # The app attempt id
    nodeId: str # The node id of the node the attempt ran on
    nodeHttpAddress: str # The node http address of the node the attempt ran on
    logsLink: str # The http link to the app attempt logs
    containerId: str # The id of the container for the app attempt
    startTime: int # The start time of the attempt (in ms since epoch)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "AppAttempt":
        return cls(
            id=d.get("id", ""),
            nodeId=d.get("nodeId", ""),
            nodeHttpAddress=d.get("nodeHttpAddress", ""),
            logsLink=d.get("logsLink", ""),
            containerId=d.get("containerId", ""),
            startTime=d.get("startTime", 0)
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ApplicationTimeout:
    type: str
    expiryTime: str
    remainingTimeInSeconds: int

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ApplicationTimeout":
        return cls(
            type=d.get("type", ""),
            expiryTime=d.get("expiryTime", ""),
            remainingTimeInSeconds=d.get("remainingTimeInSeconds", 0)
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

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

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AppContainer:
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
    def from_dict(cls, d: Dict[str, Any]) -> "AppContainer":
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

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AppState(str, Enum):
    """Possible application states"""
    NEW = "NEW"
    NEW_SAVING = "NEW_SAVING"
    SUBMITTED = "SUBMITTED"
    ACCEPTED = "ACCEPTED"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    FAILED = "FAILED"
    KILLED = "KILLED"


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

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

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


@dataclass
class AppStateResponse:
    state: AppState

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary matching the API response format"""
        return {"state": self.state.value}

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'AppStateResponse':
        """Create AppStateResponse from API response dictionary"""
        return cls(state=AppState(data.get("state", "")))


@dataclass
class KillAppRequest:
    """Request body for killing an application"""
    state: str = "KILLED"  # Only "KILLED" is allowed

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary matching the API request format"""
        return {"state": self.state}









from flask_restx import fields, Model

# Resource Request Models
resource_information_model = Model('ResourceInformation', {
    'name': fields.String(description='Resource name'),
    'value': fields.Integer(description='Resource value'),
    'units': fields.String(description='Resource units'),
    'resourceType': fields.String(description='Resource type'),
    'minimumAllocation': fields.Integer(description='Minimum allocation'),
    'maximumAllocation': fields.Integer(description='Maximum allocation')
})

resource_informations_model = Model('ResourceInformations', {
    'resourceInformation': fields.List(fields.Nested(resource_information_model), description='List of resource information')
})

resource_capability_model = Model('ResourceCapability', {
    'memory': fields.Integer(description='Memory required'),
    'vCores': fields.Integer(description='Virtual cores required'),
    'resourceInformations': fields.Nested(resource_informations_model, description='Resource information details')
})

execution_type_request_model = Model('ExecutionTypeRequest', {
    'executionType': fields.String(description='Execution type (GUARANTEED, OPPORTUNISTIC)'),
    'enforceExecutionType': fields.Boolean(description='Whether to enforce execution type')
})

resource_request_model = Model('ResourceRequest', {
    'capability': fields.Nested(resource_capability_model, description='Resource capability'),
    'nodeLabelExpression': fields.String(description='Node label expression'),
    'numContainers': fields.Integer(description='Number of containers'),
    'priority': fields.Integer(description='Priority'),
    'relaxLocality': fields.Boolean(description='Whether to relax locality'),
    'resourceName': fields.String(description='Resource name'),
    'executionTypeRequest': fields.Nested(execution_type_request_model, description='Execution type request'),
    'enforceExecutionType': fields.Boolean(description='Whether to enforce execution type')
})

# Resource Usage Models
resource_usage_model = Model('ResourceUsage', {
    'memory': fields.Integer(description='Memory used/reserved/pending'),
    'vCores': fields.Integer(description='Virtual cores used/reserved/pending'),
    'resourceInformations': fields.Nested(resource_informations_model, description='Resource information details')
})

resource_usages_by_partition_model = Model('ResourceUsagesByPartition', {
    'partitionName': fields.String(description='Partition name'),
    'used': fields.Nested(resource_usage_model, description='Used resources'),
    'reserved': fields.Nested(resource_usage_model, description='Reserved resources'),
    'pending': fields.Nested(resource_usage_model, description='Pending resources'),
    'amUsed': fields.Nested(resource_usage_model, description='AM used resources'),
    'amLimit': fields.Nested(resource_usage_model, description='AM resource limit'),
    'userAmLimit': fields.Nested(resource_usage_model, description='User AM resource limit')
})

resource_info_model = Model('ResourceInfo', {
    'resourceUsagesByPartition': fields.List(fields.Nested(resource_usages_by_partition_model), description='Resource usages by partition')
})

# Timeout Model
application_timeout_model = Model('ApplicationTimeout', {
    'type': fields.String(description='Timeout type (e.g., LIFETIME)'),
    'expiryTime': fields.String(description='Expiry time'),
    'remainingTimeInSeconds': fields.Integer(description='Remaining time in seconds')
})

# Resource Seconds Map
resource_seconds_map_entry_model = Model('ResourceSecondsMapEntry', {
    'key': fields.String(description='Resource key (e.g., memory-mb, vcores)'),
    'value': fields.String(description='Resource value')
})

# Updated Application Model
application_model = Model('Application', {
    'id': fields.String(description='Application ID'),
    'user': fields.String(description='User who submitted the application'),
    'name': fields.String(description='Application name'),
    'queue': fields.String(description='Queue name'),
    'state': fields.String(description='Application state (NEW, SUBMITTED, ACCEPTED, RUNNING, FINISHED, FAILED, KILLED)'),
    'finalStatus': fields.String(description='Final application status (UNDEFINED, SUCCEEDED, FAILED, KILLED)'),
    'progress': fields.Float(description='Application progress percentage'),
    'trackingUI': fields.String(description='Tracking UI (History or ApplicationMaster)'),
    'trackingUrl': fields.String(description='Tracking URL'),
    'diagnostics': fields.String(description='Diagnostics information'),
    'clusterId': fields.Integer(description='Cluster ID'),
    'applicationType': fields.String(description='Application type (MAPREDUCE, SPARK, etc.)'),
    'applicationTags': fields.String(description='Application tags'),
    'priority': fields.Integer(description='Application priority'),
    'startedTime': fields.Integer(description='Application start time (ms since epoch)'),
    'launchTime': fields.Integer(description='Application launch time (ms since epoch)'),
    'finishedTime': fields.Integer(description='Application finish time (ms since epoch)'),
    'elapsedTime': fields.Integer(description='Elapsed time in ms'),
    'amContainerLogs': fields.String(description='AM container logs URL'),
    'amHostHttpAddress': fields.String(description='AM host HTTP address'),
    'amRPCAddress': fields.String(description='AM RPC address'),
    'masterNodeId': fields.String(description='Master node ID'),
    'allocatedMB': fields.Integer(description='Allocated memory in MB'),
    'allocatedVCores': fields.Integer(description='Allocated virtual cores'),
    'reservedMB': fields.Integer(description='Reserved memory in MB'),
    'reservedVCores': fields.Integer(description='Reserved virtual cores'),
    'runningContainers': fields.Integer(description='Number of running containers'),
    'memorySeconds': fields.Integer(description='Memory seconds'),
    'vcoreSeconds': fields.Integer(description='VCore seconds'),
    'queueUsagePercentage': fields.Float(description='Queue usage percentage'),
    'clusterUsagePercentage': fields.Float(description='Cluster usage percentage'),
    'preemptedResourceMB': fields.Integer(description='Preempted resource memory in MB'),
    'preemptedResourceVCores': fields.Integer(description='Preempted resource virtual cores'),
    'numNonAMContainerPreempted': fields.Integer(description='Number of non-AM containers preempted'),
    'numAMContainerPreempted': fields.Integer(description='Number of AM containers preempted'),
    'preemptedMemorySeconds': fields.Integer(description='Preempted memory seconds'),
    'preemptedVcoreSeconds': fields.Integer(description='Preempted vcore seconds'),
    'logAggregationStatus': fields.String(description='Log aggregation status (DISABLED, NOT_START, RUNNING, SUCCEEDED, FAILED, TIME_OUT)'),
    'unmanagedApplication': fields.Boolean(description='Whether application is unmanaged'),
    'amNodeLabelExpression': fields.String(description='AM node label expression'),
    'resourceRequests': fields.List(fields.Nested(resource_request_model), description='Resource requests'),
    'resourceInfo': fields.Nested(resource_info_model, description='Resource information'),
    'timeouts': fields.List(fields.Nested(application_timeout_model), description='Application timeouts'),
    'resourceSecondsMap': fields.List(fields.Nested(resource_seconds_map_entry_model), description='Resource seconds map')
})

application_summary_model = Model('ApplicationSummary', {
    'id': fields.String(description='Application ID'),
    'user': fields.String(description='User who submitted the application'),
    'name': fields.String(description='Application name'),
    'queue': fields.String(description='Queue name'),
    'state': fields.String(description='Application state'),
    'finalStatus': fields.String(description='Final application status'),
    'progress': fields.Float(description='Application progress'),
    'applicationType': fields.String(description='Application type'),
    'startedTime': fields.Integer(description='Application start time'),
    'finishedTime': fields.Integer(description='Application finish time'),
    'elapsedTime': fields.Integer(description='Elapsed time'),
    'allocatedMB': fields.Integer(description='Allocated memory'),
    'allocatedVCores': fields.Integer(description='Allocated vCores'),
    'runningContainers': fields.Integer(description='Running containers'),
    'queueUsagePercentage': fields.Float(description='Queue usage percentage'),
    'clusterUsagePercentage': fields.Float(description='Cluster usage percentage')
})

app_statistics_model = Model('AppStatistics', {
    'state': fields.String(description='Application state'),
    'type': fields.String(description='Application type'),
    'count': fields.Integer(description='Number of applications')
})



app_attempt_model = Model('AppAttempt', {
    'id': fields.String(description='Attempt ID'),
    'startTime': fields.Integer(description='Start time'),
    'finishedTime': fields.Integer(description='Finish time'),
    'containerId': fields.String(description='Container ID'),
    'nodeHttpAddress': fields.String(description='Node HTTP address'),
    'nodeId': fields.String(description='Node ID'),
    'logsLink': fields.String(description='Logs link')
})



container_model = Model('Container', {
    'id': fields.String(description='Container ID'),
    'state': fields.String(description='Container state'),
    'nodeId': fields.String(description='Node ID'),
    'priority': fields.Integer(description='Priority'),
    'startedTime': fields.Integer(description='Start time'),
    'finishedTime': fields.Integer(description='Finish time'),
    'allocatedMB': fields.Integer(description='Allocated memory'),
    'allocatedVCores': fields.Integer(description='Allocated vCores')
})

# Submit Application Models
local_resource_model = Model('LocalResource', {
    'resource': fields.String(description='Resource location'),
    'type': fields.String(description='Resource type (ARCHIVE, FILE, PATTERN)'),
    'visibility': fields.String(description='Visibility (PUBLIC, PRIVATE, APPLICATION)'),
    'size': fields.Integer(description='Resource size'),
    'timestamp': fields.Integer(description='Resource timestamp')
})

am_container_spec_model = Model('AMContainerSpec', {
    'commands': fields.List(fields.String, description='Commands to execute'),
    'environment': fields.Raw(description='Environment variables'),
    'localResources': fields.Raw(description='Local resources')
})

submit_application_model = Model('SubmitApplication', {
    'applicationId': fields.String(description='Application ID'),
    'applicationName': fields.String(description='Application name'),
    'queue': fields.String(description='Queue name', default='default'),
    'priority': fields.Integer(description='Priority', default=0),
    'applicationType': fields.String(description='Application type', default='YARN'),
    'amContainerSpec': fields.Nested(am_container_spec_model, description='AM container spec'),
    'memory': fields.Integer(description='AM memory in MB', default=1024),
    'vCores': fields.Integer(description='AM virtual cores', default=1),
    'maxAppAttempts': fields.Integer(description='Max app attempts', default=2)
})

application_state_model = Model('ApplicationState', {
    'state': fields.String(description='Application state')
})



