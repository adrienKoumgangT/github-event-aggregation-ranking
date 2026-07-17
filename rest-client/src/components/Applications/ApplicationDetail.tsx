import React, { useState, useEffect } from 'react';
import {
    Box,
    Card,
    CardContent,
    Typography,
    Grid,
    Button,
    LinearProgress,
    List,
    ListItem,
    ListItemText,
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import StopIcon from '@mui/icons-material/Stop';
import StatusChip from '../Common/StatusChip';
import LoadingSpinner from '../Common/LoadingSpinner';
import ErrorAlert from '../Common/ErrorAlert';
import ConfirmDialog from '../Common/ConfirmDialog';
import { type Application } from '../../types/application';
import { applicationService } from '../../services/applicationService';
import { usePolling } from '../../hooks/usePolling';

interface ApplicationDetailProps {
    applicationId?: string;
}

const ApplicationDetail: React.FC<ApplicationDetailProps> = ({ applicationId: propId }) => {
    const { id: paramId } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const appId = propId || paramId;

    const [application, setApplication] = useState<Application | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [killDialogOpen, setKillDialogOpen] = useState(false);
    const [killing, setKilling] = useState(false);

    const fetchApplication = async () => {
        if (!appId) return;
        try {
            const data = await applicationService.getById(appId);
            setApplication(data);
            setError(null);
        } catch (err: any) {
            setError(err.message || 'Failed to fetch application');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchApplication();
    }, [appId]);

    usePolling(fetchApplication, 60000, application?.state === 'RUNNING');

    const handleKill = async () => {
        if (!appId) return;
        try {
            setKilling(true);
            await applicationService.kill(appId);
            setKillDialogOpen(false);
            await fetchApplication();
        } catch (err: any) {
            setError(err.message || 'Failed to kill application');
        } finally {
            setKilling(false);
        }
    };

    if (loading) return <LoadingSpinner />;
    if (error) return <ErrorAlert message={error} onRetry={fetchApplication} />;
    if (!application) return <Typography>Application not found</Typography>;

    const formatTimestamp = (timestamp: number) => {
        if (!timestamp) return 'N/A';
        return new Date(timestamp).toLocaleString();
    };

    const formatDuration = (ms: number) => {
        if (!ms) return 'N/A';
        const seconds = Math.floor(ms / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        return `${hours}h ${minutes % 60}m ${seconds % 60}s`;
    };

    return (
        <Box>
            <Box sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 2 }}>
                <Button
                    startIcon={<ArrowBackIcon />}
                    onClick={() => navigate('/applications')}
                >
                    Back
                </Button>
                <Typography variant="h5">
                    Application Details
                </Typography>
                {application.state === 'RUNNING' && (
                    <Button
                        variant="contained"
                        color="error"
                        startIcon={<StopIcon />}
                        onClick={() => setKillDialogOpen(true)}
                        disabled={killing}
                    >
                        Kill Application
                    </Button>
                )}
            </Box>

            <Grid container spacing={3}>
                <Grid size={{ xs: 12, md: 6 }}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" gutterBottom>
                                General Information
                            </Typography>
                            <List>
                                <ListItem>
                                    <ListItemText
                                        primary="Application ID"
                                        secondary={application.id}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Name"
                                        secondary={application.name}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="User"
                                        secondary={application.user}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Queue"
                                        secondary={application.queue}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Type"
                                        secondary={application.applicationType}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="State"
                                        secondary={<StatusChip status={application.state} />}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Final Status"
                                        secondary={application.finalStatus || 'N/A'}
                                    />
                                </ListItem>
                            </List>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid size={{ xs: 12, md: 6 }}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" gutterBottom>
                                Progress & Resources
                            </Typography>
                            <Box sx={{ mb: 2 }}>
                                <Typography variant="body2" gutterBottom>
                                    Progress: {(application.progress * 100).toFixed(1)}%
                                </Typography>
                                <LinearProgress
                                    variant="determinate"
                                    value={application.progress * 100}
                                    sx={{ height: 10, borderRadius: 5 }}
                                />
                            </Box>
                            <List>
                                <ListItem>
                                    <ListItemText
                                        primary="Allocated Memory"
                                        secondary={`${application.allocatedMB} MB`}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Allocated vCores"
                                        secondary={application.allocatedVCores}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Running Containers"
                                        secondary={application.runningContainers}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Memory Seconds"
                                        secondary={application.memorySeconds}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="vCore Seconds"
                                        secondary={application.vcoreSeconds}
                                    />
                                </ListItem>
                            </List>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid size={{ xs: 12 }}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" gutterBottom>
                                Timing
                            </Typography>
                            <List>
                                <ListItem>
                                    <ListItemText
                                        primary="Started"
                                        secondary={formatTimestamp(application.startedTime)}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Finished"
                                        secondary={formatTimestamp(application.finishedTime)}
                                    />
                                </ListItem>
                                <ListItem>
                                    <ListItemText
                                        primary="Elapsed Time"
                                        secondary={formatDuration(application.elapsedTime)}
                                    />
                                </ListItem>
                            </List>
                        </CardContent>
                    </Card>
                </Grid>

                {application.diagnostics && (
                    <Grid size={{ xs: 12 }}>
                        <Card>
                            <CardContent>
                                <Typography variant="h6" gutterBottom>
                                    Diagnostics
                                </Typography>
                                <Typography
                                    variant="body2"
                                    component="pre"
                                    sx={{
                                        whiteSpace: 'pre-wrap',
                                        wordBreak: 'break-word',
                                        backgroundColor: '#f5f5f5',
                                        p: 2,
                                        borderRadius: 1,
                                    }}
                                >
                                    {application.diagnostics}
                                </Typography>
                            </CardContent>
                        </Card>
                    </Grid>
                )}
            </Grid>

            <ConfirmDialog
                open={killDialogOpen}
                title="Kill Application"
                message={`Are you sure you want to kill application "${application.name}" (${application.id})? This action cannot be undone.`}
                confirmText="Kill"
                onConfirm={handleKill}
                onCancel={() => setKillDialogOpen(false)}
                severity="error"
            />
        </Box>
    );
};

export default ApplicationDetail;
