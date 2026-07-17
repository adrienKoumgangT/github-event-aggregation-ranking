import api from './api';
import type { ClusterInfo, ClusterMetrics, SchedulerInfo } from '../types/cluster';

export const clusterService = {
    getInfo: async (): Promise<ClusterInfo> => {
        const response = await api.get<ClusterInfo>('/cluster/info');
        return response.data;
    },

    getMetrics: async (): Promise<ClusterMetrics> => {
        const response = await api.get<ClusterMetrics>('/cluster/metrics');
        return response.data;
    },

    getScheduler: async (): Promise<SchedulerInfo> => {
        const response = await api.get<SchedulerInfo>('/cluster/scheduler');
        return response.data;
    },
};
