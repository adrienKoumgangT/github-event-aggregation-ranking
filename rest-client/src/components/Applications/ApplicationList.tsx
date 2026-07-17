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
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import RefreshIcon from '@mui/icons-material/Refresh';
import DataTable from '../Common/DataTable';
import StatusChip from '../Common/StatusChip';
import LoadingSpinner from '../Common/LoadingSpinner';
import ErrorAlert from '../Common/ErrorAlert';
import { type Application } from '../../types/application';
import { applicationService } from '../../services/applicationService';

const ApplicationList: React.FC = () => {
    const navigate = useNavigate();
    const [applications, setApplications] = useState<Application[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [statusFilter, setStatusFilter] = useState('ALL');

    const fetchApplications = async () => {
        try {
            setLoading(true);
            setError(null);
            const data = await applicationService.getAll();
            setApplications(Array.isArray(data) ? data : []);
        } catch (err: any) {
            setError(err.message || 'Failed to fetch applications');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchApplications();
        const interval = setInterval(fetchApplications, 10000);
        return () => clearInterval(interval);
    }, []);

    const filteredApps = applications.filter((app) => {
        const matchesSearch =
            app.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            app.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
            app.user.toLowerCase().includes(searchTerm.toLowerCase());

        const matchesStatus =
            statusFilter === 'ALL' || app.state === statusFilter;

        return matchesSearch && matchesStatus;
    });

    const columns = [
        {
            id: 'id',
            label: 'Application ID',
            minWidth: 200,
            format: (value: string) => (
                <Tooltip title={value}>
                    <span>{value.substring(0, 20)}...</span>
                </Tooltip>
            ),
        },
        {
            id: 'name',
            label: 'Name',
            minWidth: 150,
        },
        {
            id: 'user',
            label: 'User',
            minWidth: 100,
        },
        {
            id: 'state',
            label: 'State',
            minWidth: 100,
            format: (value: string) => <StatusChip status={value} />,
        },
        {
            id: 'applicationType',
            label: 'Type',
            minWidth: 100,
        },
        {
            id: 'progress',
            label: 'Progress',
            minWidth: 100,
            format: (value: number) => `${(value * 100).toFixed(1)}%`,
        },
        {
            id: 'allocatedMB',
            label: 'Memory (MB)',
            minWidth: 100,
            align: 'right' as const,
        },
        {
            id: 'allocatedVCores',
            label: 'vCores',
            minWidth: 100,
            align: 'right' as const,
        },
    ];

    if (loading && applications.length === 0) {
        return <LoadingSpinner />;
    }

    return (
        <Box>
            {error && (
                <ErrorAlert
                    message={error}
                    onRetry={fetchApplications}
                />
            )}

            <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid size={{ xs: 12, sm: 6, md: 4 }}>
                    <TextField
                        fullWidth
                        size="small"
                        placeholder="Search applications..."
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
                <Grid size={{ xs: 12, sm: 6, md: 4 }}>
                    <TextField
                        fullWidth
                        size="small"
                        select
                        label="Status Filter"
                        value={statusFilter}
                        onChange={(e) => setStatusFilter(e.target.value)}
                    >
                        <MenuItem value="ALL">All</MenuItem>
                        <MenuItem value="RUNNING">Running</MenuItem>
                        <MenuItem value="FINISHED">Finished</MenuItem>
                        <MenuItem value="FAILED">Failed</MenuItem>
                        <MenuItem value="KILLED">Killed</MenuItem>
                        <MenuItem value="ACCEPTED">Accepted</MenuItem>
                        <MenuItem value="SUBMITTED">Submitted</MenuItem>
                    </TextField>
                </Grid>
                <Grid size={{ xs: 12, sm: 12, md: 4 }} sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                    <Tooltip title="Refresh">
                        <IconButton onClick={fetchApplications}>
                            <RefreshIcon />
                        </IconButton>
                    </Tooltip>
                </Grid>
            </Grid>

            <DataTable
                title="Applications"
                columns={columns}
                rows={filteredApps}
                onRowClick={(row) => navigate(`/applications/${row.id}`)}
            />
        </Box>
    );
};

export default ApplicationList;
