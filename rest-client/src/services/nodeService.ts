import api from './api';
import type { Node, NodeStatistics, NodeUtilization, NodeHealth } from '../types/node';

export const nodeService = {
    getAll: async (params?: { state?: string; rack?: string }): Promise<Node[]> => {
        const response = await api.get<Node[]>('/nodes/', { params });
        return response.data;
    },

    getById: async (id: string): Promise<Node> => {
        const response = await api.get<Node>(`/nodes/${id}`);
        return response.data;
    },

    getStatistics: async (): Promise<NodeStatistics> => {
        const response = await api.get<NodeStatistics>('/nodes/statistics');
        return response.data;
    },

    getUtilization: async (id: string): Promise<NodeUtilization> => {
        const response = await api.get<NodeUtilization>(`/nodes/${id}/utilization`);
        return response.data;
    },

    getHealth: async (): Promise<NodeHealth> => {
        const response = await api.get<NodeHealth>('/nodes/health');
        return response.data;
    },
};
