export interface Node {
    id: string;
    nodeHostName: string;
    state: string;
    nodeHTTPAddress: string;
    // healthStatus: string;
    lastHealthUpdate: number;
    rack: string;
    numContainers: number;
    usedMemoryMB: number;
    availMemoryMB: number;
    usedVirtualCores: number;
    availableVirtualCores: number;
    version: string;
    resourceUtilization?: any;
}

export interface NodeStatistics {
    totalNodes: number;
    healthyNodes: number;
    unhealthyNodes: number;
    totalMemoryMB: number;
    usedMemoryMB: number;
    availableMemoryMB: number;
    memoryUtilization: number;
    totalVCores: number;
    usedVCores: number;
    availableVCores: number;
    vCoreUtilization: number;
    totalContainers: number;
    // nodes: Node[];
}

export interface NodeUtilization {
    nodeId: string;
    hostname: string;
    state: string;
    memoryUtilization: {
        total: number;
        used: number;
        available: number;
        percentage: number;
    };
    vCoreUtilization: {
        total: number;
        used: number;
        available: number;
        percentage: number;
    };
    numContainers: number;
    rack: string;
    version: string;
}

export interface NodeHealth {
    total: number;
    healthy: number;
    unhealthy: number;
    lost: number;
    decommissioned: number;
    nodes: Array<{
        id: string;
        hostname: string;
        state: string;
        healthStatus: string;
        lastHealthUpdate: number;
    }>;
}
