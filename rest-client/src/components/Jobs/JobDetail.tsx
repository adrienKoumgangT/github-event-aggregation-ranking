import React, { useState } from 'react';
import {
    Box,
    Card,
    CardContent,
    Typography,
    Grid,
    Button,
    LinearProgress,
    Chip,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import StopIcon from '@mui/icons-material/Stop';
import RefreshIcon from '@mui/icons-material/Refresh';
import StatusChip from '../Common/StatusChip';
import LoadingSpinner from '../Common/LoadingSpinner';
import ErrorAlert from '../Common/ErrorAlert';
import ConfirmDialog from '../Common/ConfirmDialog';
import JobLogs from './JobLogs';
import { useJobStatus } from '../../hooks/useJobStatus';
import { jobService } from '../../services/jobService';

interface JobDetailProps {
    jobId?: string;
}

const JobDetail: React.FC<JobDetailProps> = ({ jobId }) => {
    const navigate = useNavigate();
    const { job, loading, error, isRunning, refresh } = useJobStatus(jobId);
    const [killDialogOpen, setKillDialogOpen] = useState(false);
    const [killing, setKilling] = useState(false);

    const handleKill = async () => {
        if (!job?.jobId) return;
        try {
            setKilling(true);
            await jobService.kill(job.jobId);
            setKillDialogOpen(false);
            refresh();
        } catch (err: any) {
            console.error('Failed to kill job:', err);
        } finally {
            setKilling(false);
        }
    };

    if (loading) return <LoadingSpinner message="Loading job details..." />;
    if (error) return <ErrorAlert message={error} onRetry={refresh} />;
    if (!job) return <Typography>Job not found</Typography>;

    const formatDuration = (seconds: number) => {
        if (seconds === 0) return 'N/A';
        const h = Math.floor(seconds / 3600);
        const m = Math.floor((seconds % 3600) / 60);
        const s = seconds % 60;
        return `${h}h ${m}m ${s}s`;
    };

    return (
        <Box>
            <Box sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 2 }}>
                <Button
                    startIcon={<ArrowBackIcon />}
                    onClick={() => navigate('/jobs')}
                >
                    Back to Jobs
                </Button>
                <Typography variant="h5">
                    Job Details
                </Typography>
                <Box sx={{ flexGrow: 1 }} />
                {isRunning && (
                    <Button
                        variant="contained"
                        color="error"
                        startIcon={<StopIcon />}
                        onClick={() => setKillDialogOpen(true)}
                        disabled={killing}
                    >
                        Kill Job
                    </Button>
                )}
                <Button
                    startIcon={<RefreshIcon />}
                    onClick={refresh}
                >
                    Refresh
                </Button>
            </Box>

            <Grid container spacing={3}>
                {/* Job Info */}
                <Grid size={{ xs: 12, md: 6 }}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" gutterBottom>
                                Job Information
                            </Typography>
                            <Grid container spacing={2}>
                                <Grid size={{ xs: 6 }}>
                                    <Typography variant="caption" color="textSecondary">
                                        Job ID
                                    </Typography>
                                    <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                                        {job.jobId.substring(0, 8)}...
                                    </Typography>
                                </Grid>
                                <Grid size={{ xs: 6 }}>
                                    <Typography variant="caption" color="textSecondary">
                                        Name
                                    </Typography>
                                    <Typography variant="body2">{job.name}</Typography>
                                </Grid>
                                <Grid size={{ xs: 6 }}>
                                    <Typography variant="caption" color="textSecondary">
                                        Type
                                    </Typography>
                                    <Chip label={job.type} size="small" color="primary" />
                                </Grid>
                                <Grid size={{ xs: 6 }}>
                                    <Typography variant="caption" color="textSecondary">
                                        Status
                                    </Typography>
                                    <Box>
                                        <StatusChip status={job.status} />
                                    </Box>
                                </Grid>
                                <Grid size={{ xs: 6 }}>
                                    <Typography variant="caption" color="textSecondary">
                                        User
                                    </Typography>
                                    <Typography variant="body2">{job.user}</Typography>
                                </Grid>
                                <Grid size={{ xs: 6 }}>
                                    <Typography variant="caption" color="textSecondary">
                                        Queue
                                    </Typography>
                                    <Typography variant="body2">{job.queue}</Typography>
                                </Grid>
                                {job.applicationId && (
                                    <Grid size={{ xs: 12 }}>
                                        <Typography variant="caption" color="textSecondary">
                                            Application ID
                                        </Typography>
                                        <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                                            {job.applicationId}
                                        </Typography>
                                    </Grid>
                                )}
                            </Grid>
                        </CardContent>
                    </Card>
                </Grid>

                {/* Progress & Resources */}
                <Grid size={{ xs: 12, md: 6 }}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" gutterBottom>
                                Progress & Resources
                            </Typography>

                            <Box sx={{mb: 3}}>
                                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                    <Typography variant="body2">
                                        Progress: {job.progress.toFixed(1)}%
                                    </Typography>
                                </Box>
                                <LinearProgress
                                    variant="determinate"
                                    value={job.progress}
                                    sx={{ height: 10, borderRadius: 5 }}
                                />
                            </Box>

                            <Grid container spacing={2}>
                                <Grid size={{ xs: 6 }}>
                                    <Typography variant="caption" color="textSecondary">
                                        Memory
                                    </Typography>
                                    <Typography variant="body2">{job.memoryMB} MB</Typography>
                                </Grid>
                                <Grid size={{ xs: 6 }}>
                                    <Typography variant="caption" color="textSecondary">
                                        vCores
                                    </Typography>
                                    <Typography variant="body2">{job.vCores}</Typography>
                                </Grid>
                                <Grid size={{ xs: 6 }}>
                                    <Typography variant="caption" color="textSecondary">
                                        Priority
                                    </Typography>
                                    <Typography variant="body2">{job.priority}</Typography>
                                </Grid>
                                <Grid size={{ xs: 6 }}>
                                    <Typography variant="caption" color="textSecondary">
                                        Elapsed Time
                                    </Typography>
                                    <Typography variant="body2">
                                        {formatDuration(job.elapsedTime)}
                                    </Typography>
                                </Grid>
                            </Grid>
                        </CardContent>
                    </Card>
                </Grid>

                {/* Timing */}
                <Grid size={{ xs: 12, md: 6 }}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" gutterBottom>
                                Timing
                            </Typography>
                            <Grid container spacing={2}>
                                <Grid size={{ xs: 6 }}>
                                    <Typography variant="caption" color="textSecondary">
                                        Created
                                    </Typography>
                                    <Typography variant="body2">
                                        {new Date(job.createdAt).toLocaleString()}
                                    </Typography>
                                </Grid>
                                <Grid size={{ xs: 6 }}>
                                    <Typography variant="caption" color="textSecondary">
                                        Started
                                    </Typography>
                                    <Typography variant="body2">
                                        {job.startedAt ? new Date(job.startedAt).toLocaleString() : 'N/A'}
                                    </Typography>
                                </Grid>
                                <Grid size={{ xs: 6 }}>
                                    <Typography variant="caption" color="textSecondary">
                                        Finished
                                    </Typography>
                                    <Typography variant="body2">
                                        {job.finishedAt ? new Date(job.finishedAt).toLocaleString() : 'N/A'}
                                    </Typography>
                                </Grid>
                                <Grid size={{ xs: 6 }}>
                                    <Typography variant="caption" color="textSecondary">
                                        Final Status
                                    </Typography>
                                    <Typography variant="body2">
                                        {job.finalStatus || 'N/A'}
                                    </Typography>
                                </Grid>
                            </Grid>
                        </CardContent>
                    </Card>
                </Grid>

                {/* Configuration */}
                {job.configuration && (
                    <Grid size={{ xs: 12, md: 6 }}>
                        <Card>
                            <CardContent>
                                <Typography variant="h6" gutterBottom>
                                    Configuration
                                </Typography>
                                <Grid container spacing={1}>
                                    {Object.entries(job.configuration).map(([key, value]) => (
                                        value != null && value !== '' && !Array.isArray(value) && typeof value !== 'object' && (
                                            <Grid size={{ xs: 12 }} key={key}>
                                                <Typography variant="caption" color="textSecondary">
                                                    {key}
                                                </Typography>
                                                <Typography variant="body2">{String(value)}</Typography>
                                            </Grid>
                                        )
                                    ))}
                                    {job.configuration.arguments && job.configuration.arguments.length > 0 && (
                                        <Grid size={{ xs: 12 }}>
                                            <Typography variant="caption" color="textSecondary">
                                                Arguments
                                            </Typography>
                                            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                                                {job.configuration.arguments.map((arg: string, i: number) => (
                                                    <Chip key={i} label={arg} size="small" variant="outlined" />
                                                ))}
                                            </Box>
                                        </Grid>
                                    )}
                                </Grid>
                            </CardContent>
                        </Card>
                    </Grid>
                )}

                {/* Error Message */}
                {job.errorMessage && (
                    <Grid size={{ xs: 12 }}>
                        <Card sx={{ border: 1, borderColor: 'error.main' }}>
                            <CardContent>
                                <Typography variant="h6" color="error" gutterBottom>
                                    Error
                                </Typography>
                                <Typography
                                    variant="body2"
                                    component="pre"
                                    sx={{
                                        whiteSpace: 'pre-wrap',
                                        wordBreak: 'break-word',
                                        color: 'error.main',
                                    }}
                                >
                                    {job.errorMessage}
                                </Typography>
                            </CardContent>
                        </Card>
                    </Grid>
                )}

                {/* Logs */}
                <Grid size={{ xs: 12 }}>
                    <JobLogs jobId={job.jobId} />
                </Grid>
            </Grid>

            <ConfirmDialog
                open={killDialogOpen}
                title="Kill Job"
                message={`Are you sure you want to kill job "${job.name}"?`}
                confirmText="Kill"
                onConfirm={handleKill}
                onCancel={() => setKillDialogOpen(false)}
                severity="error"
            />
        </Box>
    );
};

export default JobDetail;
