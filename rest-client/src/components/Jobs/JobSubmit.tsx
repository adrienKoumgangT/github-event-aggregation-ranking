import React, { useState } from 'react';
import {
    Box,
    Card,
    CardContent,
    Typography,
    TextField,
    Button,
    Grid,
    Alert,
    Chip,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import SendIcon from '@mui/icons-material/Send';
import { useNavigate } from 'react-router-dom';
import type { JobType, JobSubmission } from '../../types/job';
import { jobService } from '../../services/jobService';

interface JobSubmitProps {
    jobType: JobType;
    onSuccess?: (jobId: string) => void;
}

const JobSubmit: React.FC<JobSubmitProps> = ({ jobType, onSuccess }) => {
    const navigate = useNavigate();
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [newArg, setNewArg] = useState('');

    const [config, setConfig] = useState({
        jobName: '',
        inputPath: '',
        outputPath: '',
        arguments: [] as string[],
        // Hadoop specific
        jarPath: '',
        mainClass: '',
        // Spark specific
        scriptPath: '',
        executorMemory: '1g',
        executorCores: 1,
        numExecutors: 2,
        // Common
        memory: 1024,
        vCores: 1,
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setConfig((prev) => ({
            ...prev,
            [name]: ['executorCores', 'numExecutors', 'memory', 'vCores'].includes(name)
                ? parseInt(value) || 0
                : value,
        }));
    };

    const handleAddArgument = () => {
        if (newArg.trim()) {
            setConfig((prev) => ({
                ...prev,
                arguments: [...prev.arguments, newArg.trim()],
            }));
            setNewArg('');
        }
    };

    const handleRemoveArgument = (index: number) => {
        setConfig((prev) => ({
            ...prev,
            arguments: prev.arguments.filter((_, i) => i !== index),
        }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setSubmitting(true);
        setError(null);

        try {
            const submission: JobSubmission = {
                type: jobType,
                configuration: {
                    jobName: config.jobName,
                    inputPath: config.inputPath,
                    outputPath: config.outputPath,
                    arguments: config.arguments,
                    ...(jobType === 'HADOOP' && {
                        jarPath: config.jarPath,
                        mainClass: config.mainClass,
                        memory: config.memory,
                        vCores: config.vCores,
                    }),
                    ...(jobType === 'SPARK' && {
                        scriptPath: config.scriptPath,
                        executorMemory: config.executorMemory,
                        executorCores: config.executorCores,
                        numExecutors: config.numExecutors,
                    }),
                    ...(jobType === 'PYTHON' && {
                        scriptPath: config.scriptPath,
                    }),
                },
            };

            const result = await jobService.submit(submission);

            if (onSuccess) {
                onSuccess(result.jobId);
            } else {
                navigate(`/jobs/${result.jobId}`);
            }
        } catch (err: any) {
            setError(err.message || 'Failed to submit job');
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <Card>
            <CardContent>
                <Typography variant="h6" gutterBottom>
                    {jobType} Job Configuration
                </Typography>

                {error && (
                    <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
                        {error}
                    </Alert>
                )}

                <form onSubmit={handleSubmit}>
                    <Grid container spacing={2}>
                        <Grid size={{ xs: 12}}>
                            <TextField
                                fullWidth
                                label="Job Name"
                                name="jobName"
                                value={config.jobName}
                                onChange={handleChange}
                                required
                            />
                        </Grid>

                        <Grid size={{ xs: 12, sm: 6}}>
                            <TextField
                                fullWidth
                                label="Input Path"
                                name="inputPath"
                                value={config.inputPath}
                                onChange={handleChange}
                                helperText="HDFS or local path"
                                required
                            />
                        </Grid>

                        <Grid size={{ xs: 12, sm: 6}}>
                            <TextField
                                fullWidth
                                label="Output Path"
                                name="outputPath"
                                value={config.outputPath}
                                onChange={handleChange}
                                required
                            />
                        </Grid>

                        {/* Hadoop-specific fields */}
                        {jobType === 'HADOOP' && (
                            <>
                                <Grid size={{ xs: 12, sm: 6}}>
                                    <TextField
                                        fullWidth
                                        label="JAR Path"
                                        name="jarPath"
                                        value={config.jarPath}
                                        onChange={handleChange}
                                    />
                                </Grid>
                                <Grid size={{ xs: 12, sm: 6}}>
                                    <TextField
                                        fullWidth
                                        label="Main Class"
                                        name="mainClass"
                                        value={config.mainClass}
                                        onChange={handleChange}
                                    />
                                </Grid>
                                <Grid size={{ xs: 12, sm: 6}}>
                                    <TextField
                                        fullWidth
                                        type="number"
                                        label="Memory (MB)"
                                        name="memory"
                                        value={config.memory}
                                        onChange={handleChange}
                                    />
                                </Grid>
                                <Grid size={{ xs: 12, sm: 6}}>
                                    <TextField
                                        fullWidth
                                        type="number"
                                        label="Virtual Cores"
                                        name="vCores"
                                        value={config.vCores}
                                        onChange={handleChange}
                                    />
                                </Grid>
                            </>
                        )}

                        {/* Spark-specific fields */}
                        {jobType === 'SPARK' && (
                            <>
                                <Grid size={{ xs: 12}}>
                                    <TextField
                                        fullWidth
                                        label="Script Path"
                                        name="scriptPath"
                                        value={config.scriptPath}
                                        onChange={handleChange}
                                    />
                                </Grid>
                                <Grid size={{ xs: 12, sm: 4}}>
                                    <TextField
                                        fullWidth
                                        label="Executor Memory"
                                        name="executorMemory"
                                        value={config.executorMemory}
                                        onChange={handleChange}
                                        placeholder="e.g., 1g, 512m"
                                    />
                                </Grid>
                                <Grid size={{ xs: 12, sm: 4}}>
                                    <TextField
                                        fullWidth
                                        type="number"
                                        label="Executor Cores"
                                        name="executorCores"
                                        value={config.executorCores}
                                        onChange={handleChange}
                                    />
                                </Grid>
                                <Grid size={{ xs: 12, sm: 4}}>
                                    <TextField
                                        fullWidth
                                        type="number"
                                        label="Number of Executors"
                                        name="numExecutors"
                                        value={config.numExecutors}
                                        onChange={handleChange}
                                    />
                                </Grid>
                            </>
                        )}

                        {/* Python-specific fields */}
                        {jobType === 'PYTHON' && (
                            <Grid size={{ xs: 12}}>
                                <TextField
                                    fullWidth
                                    label="Script Path"
                                    name="scriptPath"
                                    value={config.scriptPath}
                                    onChange={handleChange}
                                />
                            </Grid>
                        )}

                        {/* Arguments */}
                        <Grid size={{ xs: 12}}>
                            <Typography variant="subtitle1" gutterBottom>
                                Additional Arguments
                            </Typography>
                            <Box sx={{ display: 'flex', gap: 1, mb: 1 }}>
                                <TextField
                                    size="small"
                                    value={newArg}
                                    onChange={(e) => setNewArg(e.target.value)}
                                    onKeyPress={(e) => e.key === 'Enter' && handleAddArgument()}
                                    placeholder="Enter argument"
                                    fullWidth
                                />
                                <Button
                                    variant="outlined"
                                    onClick={handleAddArgument}
                                    startIcon={<AddIcon />}
                                >
                                    Add
                                </Button>
                            </Box>
                            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                                {config.arguments.map((arg, index) => (
                                    <Chip
                                        key={index}
                                        label={arg}
                                        onDelete={() => handleRemoveArgument(index)}
                                        size="small"
                                    />
                                ))}
                            </Box>
                        </Grid>

                        <Grid size={{ xs: 12}}>
                            <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
                                <Button
                                    type="submit"
                                    variant="contained"
                                    startIcon={<SendIcon />}
                                    disabled={submitting || !config.jobName || !config.inputPath || !config.outputPath}
                                    size="large"
                                >
                                    {submitting ? 'Submitting...' : 'Submit Job'}
                                </Button>
                            </Box>
                        </Grid>
                    </Grid>
                </form>
            </CardContent>
        </Card>
    );
};

export default JobSubmit;
