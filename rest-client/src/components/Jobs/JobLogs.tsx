import React, { useState, useEffect, useRef } from 'react';
import {
    Box,
    Card,
    CardContent,
    Typography,
    TextField,
    MenuItem,
    Grid,
    IconButton,
    Tooltip,
    Chip,
    Paper,
} from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import DownloadIcon from '@mui/icons-material/Download';
import { type JobLog } from '../../types/job';
import { jobService } from '../../services/jobService';

interface JobLogsProps {
    jobId: string;
    autoRefresh?: boolean;
}

const LOG_LEVEL_COLORS: Record<string, string> = {
    INFO: '#1976d2',
    WARN: '#ed6c02',
    ERROR: '#d32f2f',
    DEBUG: '#757575',
    SYSTEM: '#2e7d32',
    APPLICATION: '#9c27b0',
    USER: '#0288d1',
};

const JobLogs: React.FC<JobLogsProps> = ({ jobId, autoRefresh = true }) => {
    const [logs, setLogs] = useState<JobLog[]>([]);
    const [loading, setLoading] = useState(false);
    const [_error, setError] = useState<string | null>(null);
    const [logLevel, setLogLevel] = useState('ALL');
    const [logType, setLogType] = useState('ALL');
    const logsEndRef = useRef<HTMLDivElement>(null);

    const fetchLogs = async () => {
        try {
            setError(null);
            const level = logLevel === 'ALL' ? undefined : logLevel;
            const data = await jobService.getLogs(jobId, level);
            setLogs(data.logs || []);
        } catch (err: any) {
            setError(err.message || 'Failed to fetch logs');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchLogs();
    }, [jobId, logLevel]);

    useEffect(() => {
        if (autoRefresh) {
            const interval = setInterval(fetchLogs, 5000);
            return () => clearInterval(interval);
        }
    }, [autoRefresh, jobId, logLevel]);

    useEffect(() => {
        // Scroll to bottom when new logs arrive
        logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [logs]);

    const filteredLogs = logType === 'ALL'
        ? logs
        : logs.filter(log => log.type === logType);

    const handleDownload = () => {
        const logText = filteredLogs
            .map(log => `[${log.timestamp}] [${log.level}] [${log.type}] ${log.message}`)
            .join('\n');

        const blob = new Blob([logText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `job-${jobId}-logs.txt`;
        a.click();
        URL.revokeObjectURL(url);
    };

    const getLogColor = (level: string) => {
        return LOG_LEVEL_COLORS[level] || '#757575';
    };

    return (
        <Card>
            <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                    <Typography variant="h6">
                        Job Logs
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1 }}>
                        <Tooltip title="Download logs">
                            <IconButton onClick={handleDownload} size="small">
                                <DownloadIcon />
                            </IconButton>
                        </Tooltip>
                        <Tooltip title="Refresh">
                            <IconButton onClick={fetchLogs} size="small">
                                <RefreshIcon />
                            </IconButton>
                        </Tooltip>
                    </Box>
                </Box>

                <Grid container spacing={2} sx={{ mb: 2 }}>
                    <Grid size={{ xs: 6 }}>
                        <TextField
                            fullWidth
                            size="small"
                            select
                            label="Log Level"
                            value={logLevel}
                            onChange={(e) => setLogLevel(e.target.value)}
                        >
                            <MenuItem value="ALL">All Levels</MenuItem>
                            <MenuItem value="INFO">INFO</MenuItem>
                            <MenuItem value="WARN">WARN</MenuItem>
                            <MenuItem value="ERROR">ERROR</MenuItem>
                            <MenuItem value="DEBUG">DEBUG</MenuItem>
                        </TextField>
                    </Grid>
                    <Grid size={{ xs: 6 }}>
                        <TextField
                            fullWidth
                            size="small"
                            select
                            label="Log Type"
                            value={logType}
                            onChange={(e) => setLogType(e.target.value)}
                        >
                            <MenuItem value="ALL">All Types</MenuItem>
                            <MenuItem value="SYSTEM">System</MenuItem>
                            <MenuItem value="APPLICATION">Application</MenuItem>
                            <MenuItem value="USER">User</MenuItem>
                        </TextField>
                    </Grid>
                </Grid>

                <Paper
                    sx={{
                        maxHeight: 500,
                        overflow: 'auto',
                        backgroundColor: '#1e1e1e',
                        color: '#d4d4d4',
                        p: 2,
                        fontFamily: 'monospace',
                        fontSize: '0.875rem',
                    }}
                >
                    {filteredLogs.length === 0 ? (
                        <Typography color="textSecondary" align="center" sx={{ py: 4 }}>
                            No logs available
                        </Typography>
                    ) : (
                        filteredLogs.map((log, index) => (
                            <Box
                                key={log.id || index}
                                sx={{
                                    py: 0.5,
                                    borderBottom: '1px solid #333',
                                    '&:hover': {
                                        backgroundColor: '#2a2a2a',
                                    },
                                }}
                            >
                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                    <Typography
                                        variant="caption"
                                        sx={{ color: '#888', minWidth: 140 }}
                                    >
                                        {new Date(log.timestamp).toLocaleTimeString()}
                                    </Typography>
                                    <Chip
                                        label={log.level}
                                        size="small"
                                        sx={{
                                            backgroundColor: getLogColor(log.level),
                                            color: 'white',
                                            height: 20,
                                            fontSize: '0.7rem',
                                        }}
                                    />
                                    <Chip
                                        label={log.type}
                                        size="small"
                                        variant="outlined"
                                        sx={{
                                            height: 20,
                                            fontSize: '0.7rem',
                                            borderColor: '#555',
                                            color: '#aaa',
                                        }}
                                    />
                                </Box>
                                <Typography
                                    variant="body2"
                                    sx={{
                                        mt: 0.5,
                                        ml: 17,
                                        whiteSpace: 'pre-wrap',
                                        wordBreak: 'break-word',
                                        color: log.level === 'ERROR' ? '#f44336' : '#d4d4d4',
                                    }}
                                >
                                    {log.message}
                                </Typography>
                            </Box>
                        ))
                    )}
                    <div ref={logsEndRef} />
                </Paper>

                <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 1 }}>
                    <Typography variant="caption" color="textSecondary">
                        {filteredLogs.length} log entries
                    </Typography>
                    {loading && (
                        <Typography variant="caption" color="primary">
                            Refreshing...
                        </Typography>
                    )}
                </Box>
            </CardContent>
        </Card>
    );
};

export default JobLogs;
