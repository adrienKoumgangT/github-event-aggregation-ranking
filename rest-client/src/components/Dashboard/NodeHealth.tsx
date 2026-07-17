import React from 'react';
import {
    Card,
    CardContent,
    Typography,
    Box,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    Chip,
} from '@mui/material';
import {
    CheckCircle as HealthyIcon,
    Error as UnhealthyIcon,
    RemoveCircle as LostIcon,
    Block as DecommissionedIcon,
} from '@mui/icons-material';
import { type ClusterMetrics } from '../../types/cluster';

interface NodeHealthProps {
    metrics: ClusterMetrics | null;
}

const NodeHealth: React.FC<NodeHealthProps> = ({ metrics }) => {
    if (!metrics) return null;

    const nodeStatuses = [
        {
            label: 'Active Nodes',
            value: metrics.activeNodes,
            icon: <HealthyIcon color="success" />,
            color: 'success',
        },
        {
            label: 'Unhealthy Nodes',
            value: metrics.unhealthyNodes,
            icon: <UnhealthyIcon color="error" />,
            color: 'error',
        },
        {
            label: 'Lost Nodes',
            value: metrics.lostNodes,
            icon: <LostIcon color="warning" />,
            color: 'warning',
        },
        {
            label: 'Decommissioned Nodes',
            value: metrics.decommissionedNodes,
            icon: <DecommissionedIcon color="action" />,
            color: 'default',
        },
        {
            label: 'Rebooted Nodes',
            value: metrics.rebootedNodes,
            icon: <UnhealthyIcon color="info" />,
            color: 'info',
        },
    ];

    return (
        <Card>
            <CardContent>
                <Typography variant="h6" gutterBottom>
                    Node Health Status
                </Typography>
                <Box sx={{ display: 'flex', justifyContent: 'space-around', mb: 2 }}>
                    <Box sx={{ textAlign: 'center' }}>
                        <Typography variant="h3" color="primary">
                            {metrics.totalNodes}
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                            Total Nodes
                        </Typography>
                    </Box>
                </Box>
                <List>
                    {nodeStatuses.map((status) => (
                        <ListItem key={status.label}>
                            <ListItemIcon>
                                {status.icon}
                            </ListItemIcon>
                            <ListItemText primary={status.label} />
                            <Chip
                                label={status.value}
                                color={status.color as any}
                                size="small"
                            />
                        </ListItem>
                    ))}
                </List>
            </CardContent>
        </Card>
    );
};

export default NodeHealth;
