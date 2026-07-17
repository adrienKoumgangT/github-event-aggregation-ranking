import React from 'react';
import { Card, CardContent, Typography, Box, Grid } from '@mui/material';
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
} from 'recharts';
import { type ClusterMetrics } from '../../types/cluster';

interface ResourceUsageProps {
    metrics: ClusterMetrics | null;
}

const ResourceUsage: React.FC<ResourceUsageProps> = ({ metrics }) => {
    if (!metrics) return null;

    const memoryData = [
        {
            name: 'Memory (GB)',
            Used: +(metrics.allocatedMB / 1024).toFixed(2),
            Available: +(metrics.availableMB / 1024).toFixed(2),
            Total: +(metrics.totalMB / 1024).toFixed(2),
        },
    ];

    const vCoreData = [
        {
            name: 'vCores',
            Used: metrics.allocatedVirtualCores,
            Available: metrics.availableVirtualCores,
            Total: metrics.totalVirtualCores,
        },
    ];

    const containerData = [
        {
            name: 'Containers',
            Allocated: metrics.containersAllocated,
            Pending: metrics.containersPending,
            Reserved: metrics.containersReserved,
        },
    ];

    return (
        <Grid container spacing={3}>
            <Grid size={{ xs: 12, md: 6 }}>
                <Card>
                    <CardContent>
                        <Typography variant="h6" gutterBottom>
                            Memory Usage
                        </Typography>
                        <Box sx={{ width: '100%', height: 300 }}>
                            <ResponsiveContainer>
                                <BarChart data={memoryData}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="name" />
                                    <YAxis />
                                    <Tooltip />
                                    <Bar dataKey="Used" fill="#ed6c02" />
                                    <Bar dataKey="Available" fill="#2e7d32" />
                                </BarChart>
                            </ResponsiveContainer>
                        </Box>
                    </CardContent>
                </Card>
            </Grid>
            <Grid size={{ xs: 12, md: 6 }}>
                <Card>
                    <CardContent>
                        <Typography variant="h6" gutterBottom>
                            vCore Usage
                        </Typography>
                        <Box sx={{ width: '100%', height: 300 }}>
                            <ResponsiveContainer>
                                <BarChart data={vCoreData}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="name" />
                                    <YAxis />
                                    <Tooltip />
                                    <Bar dataKey="Used" fill="#9c27b0" />
                                    <Bar dataKey="Available" fill="#1976d2" />
                                </BarChart>
                            </ResponsiveContainer>
                        </Box>
                    </CardContent>
                </Card>
            </Grid>
        </Grid>
    );
};

export default ResourceUsage;
