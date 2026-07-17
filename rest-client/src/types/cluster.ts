export interface ClusterInfo {
    id: number;
    startedOn: number;
    state: string;
    hadoopVersion: string;
    resourceManagerVersion: string;
}

export interface ClusterMetrics {
    appsSubmitted: number;
    appsCompleted: number;
    appsPending: number;
    appsRunning: number;
    appsFailed: number;
    appsKilled: number;
    availableMB: number;
    allocatedMB: number;
    availableVirtualCores: number;
    allocatedVirtualCores: number;
    containersAllocated: number;
    containersReserved: number;
    containersPending: number;
    totalMB: number;
    totalVirtualCores: number;
    totalNodes: number;
    lostNodes: number;
    unhealthyNodes: number;
    decommissionedNodes: number;
    rebootedNodes: number;
    activeNodes: number;
}

export interface SchedulerInfo {
    type: string;
    capacity: any;
    queues: any;
}
