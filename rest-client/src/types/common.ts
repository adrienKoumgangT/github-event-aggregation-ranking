export interface ApiResponse<T> {
    data: T;
    status: number;
    message?: string;
}

export interface ApiError {
    error: string;
    status_code: number;
    message?: string;
}

export interface PaginationParams {
    limit?: number;
    offset?: number;
}

export interface FilterParams {
    status?: string;
    type?: string;
    user?: string;
}

export type LoadingState = 'idle' | 'loading' | 'success' | 'error';
