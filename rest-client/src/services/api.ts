import axios, { type AxiosInstance, AxiosError } from 'axios';
import type { ApiError } from '../types/common';

// Vite uses import.meta.env with VITE_ prefix
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000/api';

const api: AxiosInstance = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor
api.interceptors.request.use(
    (config) => {
        // Add auth token if available
        const token = localStorage.getItem('auth_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor
api.interceptors.response.use(
    (response) => response,
    (error: AxiosError<ApiError>) => {
        if (error.response) {
            const apiError: ApiError = {
                error: error.response.data?.error || 'An error occurred',
                status_code: error.response.status,
                message: error.response.data?.message,
            };

            // Handle specific status codes
            switch (error.response.status) {
                case 401:
                    // Handle unauthorized
                    localStorage.removeItem('auth_token');
                    window.location.href = '/login';
                    break;
                case 403:
                    console.error('Access forbidden');
                    break;
                case 404:
                    console.error('Resource not found');
                    break;
                case 500:
                    console.error('Server error');
                    break;
            }

            return Promise.reject(apiError);
        }

        return Promise.reject({
            error: 'Network error',
            status_code: 0,
            message: 'Unable to connect to server',
        });
    }
);

export default api;
