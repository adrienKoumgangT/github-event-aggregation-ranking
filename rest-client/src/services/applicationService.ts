import api from './api';
import type {
    Application,
    AppStatistics,
    AppAttempt,
    Container,
    SubmitApplication,
    ApplicationStateResponse,
} from '../types/application';

export const applicationService = {
    getAll: async (): Promise<Application[]> => {
        const response = await api.get<Application[]>('/applications/');
        return response.data;
    },

    getById: async (id: string): Promise<Application> => {
        const response = await api.get<Application>(`/applications/${id}`);
        return response.data;
    },

    getState: async (id: string): Promise<ApplicationStateResponse> => {
        const response = await api.get<ApplicationStateResponse>(`/applications/${id}/state`);
        return response.data;
    },

    kill: async (id: string): Promise<ApplicationStateResponse> => {
        const response = await api.put<ApplicationStateResponse>(
            `/applications/${id}/state`,
            { state: 'KILLED' }
        );
        return response.data;
    },

    getAttempts: async (id: string): Promise<AppAttempt[]> => {
        const response = await api.get<AppAttempt[]>(`/applications/${id}/attempts`);
        return response.data;
    },

    getStatistics: async (): Promise<AppStatistics[]> => {
        const response = await api.get<AppStatistics[]>('/applications/statistics');
        return response.data;
    },

    submit: async (app: SubmitApplication): Promise<{ message: string; applicationId: string }> => {
        const response = await api.post<{ message: string; applicationId: string }>(
            '/applications/submit',
            app
        );
        return response.data;
    },

    getContainers: async (appId: string, attemptId: string): Promise<Container[]> => {
        const response = await api.get<Container[]>(
            `/applications/${appId}/attempts/${attemptId}/containers`
        );
        return response.data;
    },
};
