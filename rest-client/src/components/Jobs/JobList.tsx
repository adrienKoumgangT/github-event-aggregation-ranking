import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Box,
    TextField,
    MenuItem,
    Grid,
    InputAdornment,
    IconButton,
    Tooltip,
    Button,
    LinearProgress,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import RefreshIcon from '@mui/icons-material/Refresh';
import AddIcon from '@mui/icons-material/Add';
import DataTable from '../Common/DataTable';
import StatusChip from '../Common/StatusChip';
import LoadingSpinner from '../Common/LoadingSpinner';
import ErrorAlert from '../Common/ErrorAlert';
import ConfirmDialog from '../Common/ConfirmDialog';
import { type Job } from '../../types/job';
import { jobService } from '../../services/jobService';

const JobList: React.FC = () => {
    const navigate = useNavigate();
    const [jobs, setJobs] = useState<Job[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [statusFilter, setStatusFilter] = useState('ALL');
    const [typeFilter, setTypeFilter] = useState('ALL');
    const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
    const [selectedJob, setSelectedJob] = useState<Job | null>(null);

    const fetchJobs = async () => {
        try {
            setError(null);
            const data = await jobService.getAll();
            setJobs(Array.isArray(data) ? data : []);
        } catch (err: any) {
            setError(err.message || 'Failed to fetch jobs');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchJobs();
        const interval = setInterval(fetchJobs, 60000);
        return () => clearInterval(interval);
    }, []);

    const handleDelete = async () => {
        if (!selectedJob) return;
        try {
            await jobService.delete(selectedJob.jobId);
            setDeleteDialogOpen(false);
            setSelectedJob(null);
            await fetchJobs();
        } catch (err: any) {
            setError(err.message || 'Failed to delete job');
        }
    };

    const filteredJobs = jobs.filter((job) => {
        const matchesSearch =
            (job.name || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
            (job.jobId || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
            (job.applicationId || '').toLowerCase().includes(searchTerm.toLowerCase());

        const matchesStatus = statusFilter === 'ALL' || job.status === statusFilter;
        const matchesType = typeFilter === 'ALL' || job.type === typeFilter;

        return matchesSearch && matchesStatus && matchesType;
    });

    const columns = [
        {
            id: 'jobId',
            label: 'Job ID',
            minWidth: 150,
            format: (value: string) => (
                <Tooltip title={value}>
                    <span>{value.substring(0, 8)}...</span>
                </Tooltip>
            ),
        },
        {
            id: 'name',
            label: 'Name',
            minWidth: 150,
        },
        {
            id: 'type',
            label: 'Type',
            minWidth: 80,
        },
        {
            id: 'status',
            label: 'Status',
            minWidth: 100,
            format: (value: string) => <StatusChip status={value} />,
        },
        {
            id: 'progress',
            label: 'Progress',
            minWidth: 150,
            format: (value: number, _row: Job) => (
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Box sx={{ flexGrow: 1 }}>
                        <LinearProgress
                            variant="determinate"
                            value={value}
                            sx={{ height: 8, borderRadius: 5 }}
                        />
                    </Box>
                    <span>{value.toFixed(1)}%</span>
                </Box>
            ),
        },
        {
            id: 'createdAt',
            label: 'Created',
            minWidth: 150,
            format: (value: string) => new Date(value).toLocaleString(),
        },
    ];

    if (loading && jobs.length === 0) {
        return <LoadingSpinner />;
    }

    return (
        <Box>
            {error && (
                <ErrorAlert message={error} onRetry={fetchJobs} />
            )}

            <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <TextField
                        fullWidth
                        size="small"
                        placeholder="Search jobs..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        slotProps={{
                            input: {
                                startAdornment: (
                                    <InputAdornment position="start">
                                        <SearchIcon />
                                    </InputAdornment>
                                ),
                            },
                            htmlInput: {
                                min: 0
                            }
                        }}
                    />
                </Grid>
                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <TextField
                        fullWidth
                        size="small"
                        select
                        label="Status"
                        value={statusFilter}
                        onChange={(e) => setStatusFilter(e.target.value)}
                    >
                        <MenuItem value="ALL">All Statuses</MenuItem>
                        <MenuItem value="PENDING">Pending</MenuItem>
                        <MenuItem value="RUNNING">Running</MenuItem>
                        <MenuItem value="FINISHED">Finished</MenuItem>
                        <MenuItem value="FAILED">Failed</MenuItem>
                        <MenuItem value="KILLED">Killed</MenuItem>
                    </TextField>
                </Grid>
                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <TextField
                        fullWidth
                        size="small"
                        select
                        label="Type"
                        value={typeFilter}
                        onChange={(e) => setTypeFilter(e.target.value)}
                    >
                        <MenuItem value="ALL">All Types</MenuItem>
                        <MenuItem value="HADOOP">Hadoop</MenuItem>
                        <MenuItem value="SPARK">Spark</MenuItem>
                        <MenuItem value="PYTHON">Python</MenuItem>
                    </TextField>
                </Grid>
                <Grid size={{ xs: 12, sm: 6, md: 3 }} sx={{ display: 'flex', justifyContent: 'flex-end', gap: 1 }}>
                    <Button
                        variant="contained"
                        startIcon={<AddIcon />}
                        onClick={() => navigate('/jobs/submit')}
                    >
                        Submit Job
                    </Button>
                    <Tooltip title="Refresh">
                        <IconButton onClick={fetchJobs}>
                            <RefreshIcon />
                        </IconButton>
                    </Tooltip>
                </Grid>
            </Grid>

            <DataTable
                title="Jobs"
                columns={columns}
                rows={filteredJobs}
                onRowClick={(row) => navigate(`/jobs/${row.jobId}`)}
            />

            <ConfirmDialog
                open={deleteDialogOpen}
                title="Delete Job"
                message={`Are you sure you want to delete job "${selectedJob?.name}"? This action cannot be undone.`}
                confirmText="Delete"
                onConfirm={handleDelete}
                onCancel={() => {
                    setDeleteDialogOpen(false);
                    setSelectedJob(null);
                }}
                severity="error"
            />
        </Box>
    );
};

export default JobList;
