export interface Application {
    id: string;
    user: string;
    name: string;
    queue: string;
    state: string;
    finalStatus: string;
    progress: number;
    trackingUI: string;
    trackingUrl: string;
    diagnostics: string;
    clusterId: number;
    applicationType: string;
    applicationTags: string;
    startedTime: number;
    finishedTime: number;
    elapsedTime: number;
    amContainerLogs: string;
    amHostHttpAddress: string;
    allocatedMB: number;
    allocatedVCores: number;
    runningContainers: number;
    memorySeconds: number;
    vcoreSeconds: number;
}

export type ApplicationState =
    | 'NEW'
    | 'NEW_SAVING'
    | 'SUBMITTED'
    | 'ACCEPTED'
    | 'RUNNING'
    | 'FINISHED'
    | 'FAILED'
    | 'KILLED';

export interface AppStatistics {
    state: string;
    type: string;
    count: number;
}

export interface AppAttempt {
    id: string;
    startTime: number;
    finishedTime: number;
    containerId: string;
    nodeHttpAddress: string;
    nodeId: string;
    logsLink: string;
}

export interface Container {
    id: string;
    state: string;
    nodeId: string;
    priority: number;
    startedTime: number;
    finishedTime: number;
    allocatedMB: number;
    allocatedVCores: number;
}

export interface SubmitApplication {
    applicationId: string;
    applicationName: string;
    queue?: string;
    priority?: number;
    applicationType?: string;
    amContainerSpec?: AMContainerSpec;
    memory?: number;
    vCores?: number;
    maxAppAttempts?: number;
}

export interface AMContainerSpec {
    commands: string[];
    environment?: Record<string, string>;
    localResources?: Record<string, LocalResource>;
}

export interface LocalResource {
    resource: string;
    type: 'ARCHIVE' | 'FILE' | 'PATTERN';
    visibility: 'PUBLIC' | 'PRIVATE' | 'APPLICATION';
    size: number;
    timestamp: number;
}

export interface ApplicationStateResponse {
    state: ApplicationState;
}
