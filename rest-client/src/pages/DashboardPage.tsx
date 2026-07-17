import React, { useState, useEffect } from 'react';
import { Box, Grid, Typography } from '@mui/material';
import ClusterOverview from '../components/Dashboard/ClusterOverview';
import ApplicationChart from '../components/Dashboard/ApplicationChart';
import ResourceUsage from '../components/Dashboard/ResourceUsage';
import NodeHealth from '../components/Dashboard/NodeHealth';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import ErrorAlert from '../components/Common/ErrorAlert';
import { type ClusterMetrics } from '../types/cluster';
import { clusterService } from '../services/clusterService';
import { usePolling } from '../hooks/usePolling';

const DashboardPage: React.FC = () => {
    const [metrics, setMetrics] = useState<ClusterMetrics | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchMetrics = async () => {
        try {
            const data = await clusterService.getMetrics();
            setMetrics(data);
            setError(null);
        } catch (err: any) {
            setError(err.message || 'Failed to fetch metrics');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchMetrics();
    }, []);

    usePolling(fetchMetrics, 5000);

    if (loading) return <LoadingSpinner message="Loading dashboard..." />;
    if (error) return <ErrorAlert message={error} onRetry={fetchMetrics} />;

    return (
        <Box>
            <Typography variant="h4" gutterBottom>
                Dashboard
            </Typography>

            <Grid container spacing={3}>
                <Grid size={{ xs: 12 }}>
                    <ClusterOverview metrics={metrics} />
                </Grid>

                <Grid size={{ xs: 12, md: 6 }}>
                    <ApplicationChart metrics={metrics} />
                </Grid>

                <Grid size={{ xs: 12, md: 6 }}>
                    <NodeHealth metrics={metrics} />
                </Grid>

                <Grid size={{ xs: 12 }}>
                    <ResourceUsage metrics={metrics} />
                </Grid>
            </Grid>
        </Box>
    );
};

export default DashboardPage;
