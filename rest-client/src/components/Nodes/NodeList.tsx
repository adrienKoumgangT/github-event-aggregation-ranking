import React, { useState, useEffect } from 'react';
import {
    Box,
    TextField,
    MenuItem,
    Grid,
    InputAdornment,
    IconButton,
    Tooltip,
    Card,
    CardContent,
    Typography,
    Chip,
    LinearProgress,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Button,
    List,
    ListItem,
    ListItemText,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import RefreshIcon from '@mui/icons-material/Refresh';
import InfoIcon from '@mui/icons-material/Info';
import StatusChip from '../Common/StatusChip';
import LoadingSpinner from '../Common/LoadingSpinner';
import ErrorAlert from '../Common/ErrorAlert';
import { type Node } from '../../types/node';
import { nodeService } from '../../services/nodeService';

const NodeList: React.FC = () => {
    const [nodes, setNodes] = useState<Node[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [stateFilter, setStateFilter] = useState('ALL');
    const [healthFilter, setHealthFilter] = useState('ALL');
    const [selectedNode, setSelectedNode] = useState<Node | null>(null);
    const [detailOpen, setDetailOpen] = useState(false);

    const fetchNodes = async () => {
        try {
            const data = await nodeService.getAll();
            setNodes(Array.isArray(data) ? data : []);
            setError(null);
        } catch (err: any) {
            setError(err.message || 'Failed to fetch nodes');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchNodes();
        const interval = setInterval(fetchNodes, 15000);
        return () => clearInterval(interval);
    }, []);

    const filteredNodes = nodes.filter((node) => {
        const matchesSearch =
            node.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
            node.nodeHostName.toLowerCase().includes(searchTerm.toLowerCase()) ||
            node.rack.toLowerCase().includes(searchTerm.toLowerCase());

        const matchesState = stateFilter === 'ALL' || node.state === stateFilter;
        const matchesHealth = healthFilter === 'ALL';

        return matchesSearch && matchesState && matchesHealth;
    });

    const getMemoryUsagePercentage = (node: Node) => {
        const total = node.usedMemoryMB + node.availMemoryMB;
        return total > 0 ? (node.usedMemoryMB / total) * 100 : 0;
    };

    const getVCoreUsagePercentage = (node: Node) => {
        const total = node.usedVirtualCores + node.availableVirtualCores;
        return total > 0 ? (node.usedVirtualCores / total) * 100 : 0;
    };

    if (loading && nodes.length === 0) {
        return <LoadingSpinner />;
    }

    return (
        <Box>
            {error && (
                <ErrorAlert message={error} onRetry={fetchNodes} />
            )}

            <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid size={{ xs: 12, sm: 6, md: 4 }}>
                    <TextField
                        fullWidth
                        size="small"
                        placeholder="Search nodes..."
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
                        label="State"
                        value={stateFilter}
                        onChange={(e) => setStateFilter(e.target.value)}
                    >
                        <MenuItem value="ALL">All States</MenuItem>
                        <MenuItem value="RUNNING">Running</MenuItem>
                        <MenuItem value="UNHEALTHY">Unhealthy</MenuItem>
                        <MenuItem value="REBOOTED">Rebooted</MenuItem>
                        <MenuItem value="LOST">Lost</MenuItem>
                        <MenuItem value="DECOMMISSIONED">Decommissioned</MenuItem>
                    </TextField>
                </Grid>
                <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                    <TextField
                        fullWidth
                        size="small"
                        select
                        label="Health"
                        value={healthFilter}
                        onChange={(e) => setHealthFilter(e.target.value)}
                    >
                        <MenuItem value="ALL">All Health</MenuItem>
                        <MenuItem value="Healthy">Healthy</MenuItem>
                        <MenuItem value="Unhealthy">Unhealthy</MenuItem>
                    </TextField>
                </Grid>
                <Grid size={{ xs: 12, sm: 6, md: 2 }} sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                    <Tooltip title="Refresh">
                        <IconButton onClick={fetchNodes}>
                            <RefreshIcon />
                        </IconButton>
                    </Tooltip>
                </Grid>
            </Grid>

            <Grid container spacing={2}>
                {filteredNodes.map((node) => (
                    <Grid size={{ xs: 12, sm: 6, md: 4 }} key={node.id}>
                        <Card
                            sx={{
                                cursor: 'pointer',
                                '&:hover': { boxShadow: 3 },
                                border: 1,
                                borderColor: node.state === 'NEW' || node.state === 'RUNNING' ? 'success.light' : 'error.light',
                            }}
                            onClick={() => {
                                setSelectedNode(node);
                                setDetailOpen(true);
                            }}
                        >
                            <CardContent>
                                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                                    <Box>
                                        <Typography variant="subtitle1" noWrap>
                                            {node.nodeHostName || node.id}
                                        </Typography>
                                        <Typography variant="caption" color="textSecondary">
                                            {node.rack}
                                        </Typography>
                                    </Box>
                                    <Box sx={{ display: 'flex', gap: 1 }}>
                                        <StatusChip status={node.state} />
                                    </Box>
                                </Box>

                                <Box sx={{mb: 2}}>
                                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                                        <Typography variant="caption">Memory</Typography>
                                        <Typography variant="caption">
                                            {(node.usedMemoryMB / 1024).toFixed(1)} / {((node.usedMemoryMB + node.availMemoryMB) / 1024).toFixed(1)} GB
                                        </Typography>
                                    </Box>
                                    <LinearProgress
                                        variant="determinate"
                                        value={getMemoryUsagePercentage(node)}
                                        sx={{ height: 6, borderRadius: 3 }}
                                    />
                                </Box>

                                <Box sx={{ mb: 2 }}>
                                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                                        <Typography variant="caption">vCores</Typography>
                                        <Typography variant="caption">
                                            {node.usedVirtualCores} / {node.usedVirtualCores + node.availableVirtualCores}
                                        </Typography>
                                    </Box>
                                    <LinearProgress
                                        variant="determinate"
                                        value={getVCoreUsagePercentage(node)}
                                        color="secondary"
                                        sx={{ height: 6, borderRadius: 3 }}
                                    />
                                </Box>

                                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                                    <Chip
                                        label={`${node.numContainers} containers`}
                                        size="small"
                                        variant="outlined"
                                    />
                                    <Tooltip title="View Details">
                                        <IconButton size="small">
                                            <InfoIcon />
                                        </IconButton>
                                    </Tooltip>
                                </Box>
                            </CardContent>
                        </Card>
                    </Grid>
                ))}
            </Grid>

            <Dialog
                open={detailOpen}
                onClose={() => setDetailOpen(false)}
                maxWidth="md"
                fullWidth
            >
                <DialogTitle>
                    Node Details: {selectedNode?.nodeHostName || selectedNode?.id}
                </DialogTitle>
                <DialogContent>
                    {selectedNode && (
                        <List>
                            <ListItem>
                                <ListItemText
                                    primary="Node ID"
                                    secondary={selectedNode.id}
                                />
                            </ListItem>
                            <ListItem>
                                <ListItemText
                                    primary="Hostname"
                                    secondary={selectedNode.nodeHostName}
                                />
                            </ListItem>
                            <ListItem>
                                <ListItemText
                                    primary="HTTP Address"
                                    secondary={selectedNode.nodeHTTPAddress}
                                />
                            </ListItem>
                            <ListItem>
                                <ListItemText
                                    primary="State"
                                    secondary={<StatusChip status={selectedNode.state} />}
                                />
                            </ListItem>
                            <ListItem>
                                <ListItemText
                                    primary="Rack"
                                    secondary={selectedNode.rack}
                                />
                            </ListItem>
                            <ListItem>
                                <ListItemText
                                    primary="Version"
                                    secondary={selectedNode.version}
                                />
                            </ListItem>
                            <ListItem>
                                <ListItemText
                                    primary="Memory"
                                    secondary={`Used: ${(selectedNode.usedMemoryMB / 1024).toFixed(1)} GB / Available: ${(selectedNode.availMemoryMB / 1024).toFixed(1)} GB`}
                                />
                            </ListItem>
                            <ListItem>
                                <ListItemText
                                    primary="vCores"
                                    secondary={`Used: ${selectedNode.usedVirtualCores} / Available: ${selectedNode.availableVirtualCores}`}
                                />
                            </ListItem>
                            <ListItem>
                                <ListItemText
                                    primary="Containers"
                                    secondary={selectedNode.numContainers}
                                />
                            </ListItem>
                            <ListItem>
                                <ListItemText
                                    primary="Last Health Update"
                                    secondary={new Date(selectedNode.lastHealthUpdate).toLocaleString()}
                                />
                            </ListItem>
                        </List>
                    )}
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setDetailOpen(false)}>Close</Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
};

export default NodeList;
