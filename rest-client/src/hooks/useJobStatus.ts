import { useState, useEffect, useCallback } from 'react';
import type { Job, JobStatus } from '../types/job';
import { jobService } from '../services/jobService';

interface UseJobStatusReturn {
    job: Job | null;
    loading: boolean;
    error: string | null;
    isRunning: boolean;
    refresh: () => Promise<void>;
}

export function useJobStatus(
    jobId: string | undefined,
    pollInterval: number = 5000
): UseJobStatusReturn {
    const [job, setJob] = useState<Job | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const runningStates: JobStatus[] = ['PENDING', 'RUNNING'];
    const isRunning = job ? runningStates.includes(job.status) : false;

    const fetchJob = useCallback(async () => {
        if (!jobId) return;

        try {
            setLoading(true);
            setError(null);
            const data = await jobService.getStatus(jobId);
            setJob(data);
        } catch (err: any) {
            setError(err.message || 'Failed to fetch job status');
        } finally {
            setLoading(false);
        }
    }, [jobId]);

    useEffect(() => {
        fetchJob();
    }, [fetchJob]);

    // Poll for updates if job is running
    useEffect(() => {
        if (!isRunning) return;

        const interval = setInterval(fetchJob, pollInterval);
        return () => clearInterval(interval);
    }, [isRunning, pollInterval, fetchJob]);

    return { job, loading, error, isRunning, refresh: fetchJob };
}
