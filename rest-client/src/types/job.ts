export type JobType = 'HADOOP' | 'SPARK' | 'PYTHON';

export type JobStatus =
    | 'PENDING'
    | 'RUNNING'
    | 'FINISHED'
    | 'FAILED'
    | 'KILLED'
    | 'CANCELLED';

export interface JobTypeInfo {
    type: JobType;
    displayName: string;
    description: string;
    parameters: JobParameter[];
}

export interface JobParameter {
    name: string;
    label: string;
    type: 'text' | 'number' | 'array';
    required: boolean;
    default?: any;
}

export interface Job {
    jobId: string;
    name: string;
    type: JobType;
    status: JobStatus;
    progress: number;
    applicationId?: string;
    applicationUrl?: string;
    createdAt: string;
    startedAt?: string;
    finishedAt?: string;
    user: string;
    queue: string;
    priority: number;
    memoryMB: number;
    vCores: number;
    inputPath: string;
    outputPath: string;
    finalStatus?: string;
    diagnostics?: string;
    errorMessage?: string;
    elapsedTime: number;
    configuration?: JobConfiguration;
    logs?: JobLog[];
}

export interface JobConfiguration {
    jarPath?: string;
    mainClass?: string;
    scriptPath?: string;
    executorMemory?: string;
    executorCores?: number;
    numExecutors?: number;
    sparkMaster?: string;
    deployMode?: string;
    pythonScriptPath?: string;
    pythonExecutable?: string;
    arguments: string[];
    environmentVars: Record<string, string>;
    additionalParams: Record<string, any>;
}

export interface JobLog {
    id: number;
    timestamp: string;
    level: string;
    message: string;
    type: string;
}

export interface JobSubmission {
    type: JobType;
    configuration: Record<string, any>;
    user?: string;
    queue?: string;
    priority?: number;
}

export interface JobResult {
    jobId: string;
    status: JobStatus;
    finalStatus?: string;
    outputPath: string;
    diagnostics?: string;
    errorMessage?: string;
    logs: JobLog[];
}

export interface JobStatistics {
    totalJobs: number;
    statusDistribution: Record<string, number>;
    typeDistribution: Record<string, number>;
    recentJobs: Job[];
}
