import React from 'react';
import {
    Card,
    CardContent,
    Typography,
    Grid,
    Box,
    LinearProgress,
    Tooltip,
} from '@mui/material';
import {
    Dns as DnsIcon,
    Memory as MemoryIcon,
    DeveloperBoard as CpuIcon,
    CheckCircle as HealthyIcon,
    Error as UnhealthyIcon,
} from '@mui/icons-material';
import { type NodeStatistics } from '../../types/node';

interface NodeUtilizationProps {
    statistics: NodeStatistics;
}

interface MetricCardProps {
    title: string;
    value: string | number;
    total: string | number;
    percentage: number;
    icon: React.ReactElement;
    color: string;
}

const MetricCard: React.FC<MetricCardProps> = (
    {
        title,
        value,
        total,
        percentage,
        icon,
        color,
    }
) => (
    <Card>
        <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Box sx={{ color }}>
                        {icon}
                    </Box>
                    <Typography variant="subtitle1" color="textSecondary">
                        {title}
                    </Typography>
                </Box>
            </Box>

            <Box sx={{ mb: 1 }}>
                <Typography variant="h4" gutterBottom>
                    {value}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                    of {total} total
                </Typography>
            </Box>

            <Tooltip title={`${percentage.toFixed(1)}% utilized`}>
                <Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                        <Typography variant="caption" color="textSecondary">
                            Utilization
                        </Typography>
                        <Typography variant="caption" color="textSecondary">
                            {percentage.toFixed(1)}%
                        </Typography>
                    </Box>
                    <LinearProgress
                        variant="determinate"
                        value={percentage}
                        sx={{
                            height: 8,
                            borderRadius: 5,
                            backgroundColor: `${color}20`,
                            '& .MuiLinearProgress-bar': {
                                backgroundColor: color,
                            },
                        }}
                    />
                </Box>
            </Tooltip>
        </CardContent>
    </Card>
);

const NodeUtilization: React.FC<NodeUtilizationProps> = ({ statistics }) => {
    return (
        <Grid container spacing={3}>
            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <MetricCard
                    title="Nodes"
                    value={statistics.healthyNodes}
                    total={statistics.totalNodes}
                    percentage={(statistics.healthyNodes / statistics.totalNodes) * 100}
                    icon={<DnsIcon />}
                    color="#1976d2"
                />
            </Grid>

            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <MetricCard
                    title="Memory"
                    value={`${(statistics.usedMemoryMB / 1024).toFixed(1)} GB`}
                    total={`${(statistics.totalMemoryMB / 1024).toFixed(1)} GB`}
                    percentage={statistics.memoryUtilization}
                    icon={<MemoryIcon />}
                    color="#ed6c02"
                />
            </Grid>

            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <MetricCard
                    title="vCores"
                    value={statistics.usedVCores}
                    total={statistics.totalVCores}
                    percentage={statistics.vCoreUtilization}
                    icon={<CpuIcon />}
                    color="#9c27b0"
                />
            </Grid>

            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                <Card>
                    <CardContent>
                        <Typography variant="subtitle1" color="textSecondary" gutterBottom>
                            Health Status
                        </Typography>

                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                            <HealthyIcon color="success" />
                            <Box>
                                <Typography variant="h6">{statistics.healthyNodes}</Typography>
                                <Typography variant="caption" color="textSecondary">Healthy</Typography>
                            </Box>
                        </Box>

                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <UnhealthyIcon color="error" />
                            <Box>
                                <Typography variant="h6">{statistics.unhealthyNodes}</Typography>
                                <Typography variant="caption" color="textSecondary">Unhealthy</Typography>
                            </Box>
                        </Box>

                        <Box sx={{ mt: 2 }}>
                            <Typography variant="body2" color="textSecondary">
                                Total Containers: {statistics.totalContainers}
                            </Typography>
                        </Box>
                    </CardContent>
                </Card>
            </Grid>
        </Grid>
    );
};

export default NodeUtilization;
