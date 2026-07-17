import React from 'react';
import { Grid, Card, CardContent, Typography, Box } from '@mui/material';
import {
    Dns as DnsIcon,
    Apps as AppsIcon,
    Memory as MemoryIcon,
    DeveloperBoard as CpuIcon,
} from '@mui/icons-material';
import { type ClusterMetrics } from '../../types/cluster';

interface ClusterOverviewProps {
    metrics: ClusterMetrics | null;
}

interface StatCardProps {
    title: string;
    value: string | number;
    subtitle?: string;
    icon: React.ReactElement;
    color: string;
}

const StatCard: React.FC<StatCardProps> = ({ title, value, subtitle, icon, color }) => (
    <Card>
        <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                    <Typography variant="body2" color="textSecondary" gutterBottom>
                        {title}
                    </Typography>
                    <Typography variant="h4" component="div">
                        {value}
                    </Typography>
                    {subtitle && (
                        <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                            {subtitle}
                        </Typography>
                    )}
                </Box>
                <Box
                    sx={{
                        backgroundColor: color,
                        borderRadius: '50%',
                        p: 1.5,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: 'white',
                        '& .MuiSvgIcon-root': {
                            fontSize: 30,
                            color: 'white',
                        },
                    }}
                >
                    {icon}
                </Box>
            </Box>
        </CardContent>
    </Card>
);

const ClusterOverview: React.FC<ClusterOverviewProps> = ({ metrics }) => {
    if (!metrics) return null;

    return (
        <Grid container spacing={3}>
            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <StatCard
                    title="Active Nodes"
                    value={metrics.activeNodes}
                    subtitle={`${metrics.lostNodes} lost, ${metrics.unhealthyNodes} unhealthy`}
                    icon={<DnsIcon />}
                    color="#1976d2"
                />
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <StatCard
                    title="Running Apps"
                    value={metrics.appsRunning}
                    subtitle={`${metrics.appsPending} pending, ${metrics.appsSubmitted} submitted`}
                    icon={<AppsIcon />}
                    color="#2e7d32"
                />
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <StatCard
                    title="Memory"
                    value={`${(metrics.availableMB / 1024).toFixed(1)} GB`}
                    subtitle={`${(metrics.allocatedMB / 1024).toFixed(1)} GB allocated`}
                    icon={<MemoryIcon />}
                    color="#ed6c02"
                />
            </Grid>
            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <StatCard
                    title="vCores"
                    value={metrics.availableVirtualCores}
                    subtitle={`${metrics.allocatedVirtualCores} allocated`}
                    icon={<CpuIcon />}
                    color="#9c27b0"
                />
            </Grid>
        </Grid>
    );
};

export default ClusterOverview;
