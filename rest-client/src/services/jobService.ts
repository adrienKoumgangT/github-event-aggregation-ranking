import api from './api';
import type {
    Job,
    JobTypeInfo,
    JobSubmission,
    JobResult,
    JobStatistics,
} from '../types/job';
import type { FilterParams, PaginationParams } from '../types/common';

export const jobService = {
    getTypes: async (): Promise<JobTypeInfo[]> => {
        const response = await api.get<JobTypeInfo[]>('/jobs/types');
        return response.data;
    },

    submit: async (job: JobSubmission): Promise<{ jobId: string; status: string; message: string }> => {
        const response = await api.post<{ jobId: string; status: string; message: string }>(
            '/jobs/submit',
            job
        );
        return response.data;
    },

    getStatus: async (id: string): Promise<Job> => {
        const response = await api.get<Job>(`/jobs/${id}`);
        return response.data;
    },

    getAll: async (params?: FilterParams & PaginationParams): Promise<Job[]> => {
        const response = await api.get<Job[]>('/jobs', { params });
        return response.data;
    },

    getResult: async (id: string): Promise<JobResult> => {
        const response = await api.get<JobResult>(`/jobs/${id}/result`);
        return response.data;
    },

    kill: async (id: string): Promise<{ jobId: string; status: string; message: string }> => {
        const response = await api.put<{ jobId: string; status: string; message: string }>(
            `/jobs/${id}/kill`
        );
        return response.data;
    },

    getLogs: async (id: string, logLevel?: string): Promise<{ jobId: string; logs: any[] }> => {
        const response = await api.get<{ jobId: string; logs: any[] }>(
            `/jobs/${id}/logs`,
            { params: { log_level: logLevel } }
        );
        return response.data;
    },

    getStatistics: async (): Promise<JobStatistics> => {
        const response = await api.get<JobStatistics>('/jobs/statistics');
        return response.data;
    },

    delete: async (id: string): Promise<{ message: string }> => {
        const response = await api.delete<{ message: string }>(`/jobs/${id}`);
        return response.data;
    },
};
