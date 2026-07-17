import React, { useState, useEffect } from 'react';
import {
    Box,
    Card,
    CardContent,
    Typography,
    Grid,
    List,
    ListItem,
    ListItemText,
    LinearProgress,
    Button,
} from '@mui/material';
import { useNavigate, useParams } from 'react-router-dom';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import StatusChip from '../Common/StatusChip';
import LoadingSpinner from '../Common/LoadingSpinner';
import ErrorAlert from '../Common/ErrorAlert';
import type { Node, NodeUtilization as NodeUtilizationType } from '../../types/node';
import { nodeService } from '../../services/nodeService';
import { usePolling } from '../../hooks/usePolling';

interface NodeDetailProps {
    nodeId?: string;
}

const NodeDetail: React.FC<NodeDetailProps> = ({ nodeId: propId }) => {
    const { id: paramId } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const nodeId = propId || paramId;

    const [node, setNode] = useState<Node | null>(null);
    const [utilization, setUtilization] = useState<NodeUtilizationType | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchNodeData = async () => {
        if (!nodeId) return;
        try {
            const [nodeData, utilData] = await Promise.all([
                nodeService.getById(nodeId),
                nodeService.getUtilization(nodeId),
            ]);
            setNode(nodeData);
            setUtilization(utilData);
            setError(null);
        } catch (err: any) {
            setError(err.message || 'Failed to fetch node data');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchNodeData();
    }, [nodeId]);

    usePolling(fetchNodeData, 10000);

    if (loading) return <LoadingSpinner />;
    if (error) return <ErrorAlert message={error} onRetry={fetchNodeData} />;
    if (!node) return <Typography>Node not found</Typography>;

    return (
        <Box>
            <Box sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 2 }}>
                <Button
                    startIcon={<ArrowBackIcon />}
                    onClick={() => navigate('/nodes')}
                >
                    Back to Nodes
                </Button>
                <Typography variant="h5">
                    Node Details
                </Typography>
            </Box>

            <Grid container spacing={3}>
                <Grid size={{ xs: 12, md: 6 }} >
                    <Card>
                        <CardContent>
                            <Typography variant="h6" gutterBottom>
                                General Information
                            </Typography>
                            <List>
                                <ListItem>
                                    <ListItemText
                                        primary="Node ID"
                                        secondary={node.id}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Hostname"
                                        secondary={node.nodeHostName}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="HTTP Address"
                                        secondary={node.nodeHTTPAddress}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Rack"
                                        secondary={node.rack}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Version"
                                        secondary={node.version}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="State"
                                        secondary={<StatusChip status={node.state} />}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Last Health Update"
                                        secondary={new Date(node.lastHealthUpdate).toLocaleString()}
                                    />
                                </ListItem>
                            </List>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid size={{ xs: 12, md: 6 }} >
                    <Card>
                        <CardContent>
                            <Typography variant="h6" gutterBottom>
                                Resource Utilization
                            </Typography>

                            {utilization && (
                                <>
                                    <Box sx={{ mb: 3 }}>
                                        <Typography variant="subtitle2" gutterBottom>
                                            Memory Usage
                                        </Typography>
                                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                            <Typography variant="body2">
                                                Used: {(utilization.memoryUtilization.used / 1024).toFixed(1)} GB
                                            </Typography>
                                            <Typography variant="body2">
                                                Available: {(utilization.memoryUtilization.available / 1024).toFixed(1)} GB
                                            </Typography>
                                        </Box>
                                        <LinearProgress
                                            variant="determinate"
                                            value={utilization.memoryUtilization.percentage}
                                            sx={{ height: 10, borderRadius: 5 }}
                                        />
                                        <Typography variant="caption" color="textSecondary">
                                            {utilization.memoryUtilization.percentage.toFixed(1)}% utilized
                                        </Typography>
                                    </Box>

                                    <Box sx={{ mb: 3 }}>
                                        <Typography variant="subtitle2" gutterBottom>
                                            vCore Usage
                                        </Typography>
                                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                            <Typography variant="body2">
                                                Used: {utilization.vCoreUtilization.used}
                                            </Typography>
                                            <Typography variant="body2">
                                                Available: {utilization.vCoreUtilization.available}
                                            </Typography>
                                        </Box>
                                        <LinearProgress
                                            variant="determinate"
                                            value={utilization.vCoreUtilization.percentage}
                                            color="secondary"
                                            sx={{ height: 10, borderRadius: 5 }}
                                        />
                                        <Typography variant="caption" color="textSecondary">
                                            {utilization.vCoreUtilization.percentage.toFixed(1)}% utilized
                                        </Typography>
                                    </Box>

                                    <Box>
                                        <Typography variant="subtitle2" gutterBottom>
                                            Containers
                                        </Typography>
                                        <Typography variant="h4">
                                            {utilization.numContainers}
                                        </Typography>
                                    </Box>
                                </>
                            )}
                        </CardContent>
                    </Card>
                </Grid>

                <Grid size={{ xs: 12 }}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" gutterBottom>
                                Resource Details
                            </Typography>
                            <Grid container spacing={2}>
                                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                                    <Card variant="outlined">
                                        <CardContent>
                                            <Typography variant="caption" color="textSecondary">
                                                Used Memory
                                            </Typography>
                                            <Typography variant="h6">
                                                {(node.usedMemoryMB / 1024).toFixed(1)} GB
                                            </Typography>
                                        </CardContent>
                                    </Card>
                                </Grid>
                                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                                    <Card variant="outlined">
                                        <CardContent>
                                            <Typography variant="caption" color="textSecondary">
                                                Available Memory
                                            </Typography>
                                            <Typography variant="h6">
                                                {(node.availMemoryMB / 1024).toFixed(1)} GB
                                            </Typography>
                                        </CardContent>
                                    </Card>
                                </Grid>
                                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                                    <Card variant="outlined">
                                        <CardContent>
                                            <Typography variant="caption" color="textSecondary">
                                                Used vCores
                                            </Typography>
                                            <Typography variant="h6">
                                                {node.usedVirtualCores}
                                            </Typography>
                                        </CardContent>
                                    </Card>
                                </Grid>
                                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                                    <Card variant="outlined">
                                        <CardContent>
                                            <Typography variant="caption" color="textSecondary">
                                                Available vCores
                                            </Typography>
                                            <Typography variant="h6">
                                                {node.availableVirtualCores}
                                            </Typography>
                                        </CardContent>
                                    </Card>
                                </Grid>
                            </Grid>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </Box>
    );
};

export default NodeDetail;
