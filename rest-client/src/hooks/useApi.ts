import { useState, useCallback } from 'react';
import type { LoadingState } from '../types/common';

interface UseApiReturn<T> {
    data: T | null;
    loading: LoadingState;
    error: string | null;
    execute: (...args: any[]) => Promise<T>;
}

export function useApi<T>(
    apiFunc: (...args: any[]) => Promise<T>
): UseApiReturn<T> {
    const [data, setData] = useState<T | null>(null);
    const [loading, setLoading] = useState<LoadingState>('idle');
    const [error, setError] = useState<string | null>(null);

    const execute = useCallback(async (...args: any[]): Promise<T> => {
        try {
            setLoading('loading');
            setError(null);
            const result = await apiFunc(...args);
            setData(result);
            setLoading('success');
            return result;
        } catch (err: any) {
            const errorMessage = err.message || err.error || 'An error occurred';
            setError(errorMessage);
            setLoading('error');
            throw err;
        }
    }, [apiFunc]);

    return { data, loading, error, execute };
}
