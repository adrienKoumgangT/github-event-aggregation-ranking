import React, { useState, useEffect } from 'react';
import { Box, Typography, Grid } from '@mui/material';
import NodeList from '../components/Nodes/NodeList';
import NodeUtilization from '../components/Nodes/NodeUtilization';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import ErrorAlert from '../components/Common/ErrorAlert';
import { type NodeStatistics } from '../types/node';
import { nodeService } from '../services/nodeService';
import { usePolling } from '../hooks/usePolling';

const NodesPage: React.FC = () => {
    const [statistics, setStatistics] = useState<NodeStatistics | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchStatistics = async () => {
        try {
            const data = await nodeService.getStatistics();
            setStatistics(data);
            setError(null);
        } catch (err: any) {
            setError(err.message || 'Failed to fetch node statistics');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchStatistics();
    }, []);

    usePolling(fetchStatistics, 60000);

    if (loading) return <LoadingSpinner message="Loading nodes..." />;

    return (
        <Box>
            <Typography variant="h4" gutterBottom>
                Cluster Nodes
            </Typography>

            {error && (
                <ErrorAlert message={error} onRetry={fetchStatistics} />
            )}

            {statistics && (
                <>
                    <Grid container spacing={3} sx={{ mb: 3 }}>
                        <Grid size={{ xs: 12 }}>
                            <NodeUtilization statistics={statistics} />
                        </Grid>
                    </Grid>

                    <Grid container spacing={3}>
                        <Grid size={{ xs: 12 }}>
                            <NodeList />
                        </Grid>
                    </Grid>
                </>
            )}
        </Box>
    );
};

export default NodesPage;
