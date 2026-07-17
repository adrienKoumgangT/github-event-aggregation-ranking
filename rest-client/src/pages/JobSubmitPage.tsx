import React, { useState } from 'react';
import {
    Box,
    Typography,
    Stepper,
    Step,
    StepLabel,
    Button,
    Card,
    CardContent,
    TextField,
    Grid,
    Alert,
    Chip,
    IconButton,
    List,
    ListItem,
    ListItemText,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import SendIcon from '@mui/icons-material/Send';
import { useNavigate } from 'react-router-dom';
import JobTypeSelector from '../components/Jobs/JobTypeSelector';
import type { JobType, JobSubmission } from '../types/job';
import { jobService } from '../services/jobService';

const steps = ['Select Job Type', 'Configure Job', 'Review & Submit'];

interface JobConfig {
    jobName: string;
    inputPath: string;
    outputPath: string;
    arguments: string[];
    // Hadoop specific
    jarPath?: string;
    mainClass?: string;
    // Spark specific
    scriptPath?: string;
    executorMemory?: string;
    executorCores?: number;
    numExecutors?: number;
    // Common
    memory?: number;
    vCores?: number;
}

const JobSubmitPage: React.FC = () => {
    const navigate = useNavigate();
    const [activeStep, setActiveStep] = useState(0);
    const [jobType, setJobType] = useState<JobType | null>(null);
    const [config, setConfig] = useState<JobConfig>({
        jobName: '',
        inputPath: '',
        outputPath: '',
        arguments: [],
    });
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [newArg, setNewArg] = useState('');

    const handleNext = () => {
        setActiveStep((prev) => prev + 1);
    };

    const handleBack = () => {
        setActiveStep((prev) => prev - 1);
    };

    const handleConfigChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setConfig((prev) => ({
            ...prev,
            [name]: value,
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

    const handleSubmit = async () => {
        if (!jobType) return;

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
                        executorMemory: config.executorMemory || '1g',
                        executorCores: config.executorCores || 1,
                        numExecutors: config.numExecutors || 2,
                    }),
                    ...(jobType === 'PYTHON' && {
                        scriptPath: config.scriptPath,
                    }),
                },
            };

            const result = await jobService.submit(submission);
            navigate(`/jobs/${result.jobId}`);
        } catch (err: any) {
            setError(err.message || 'Failed to submit job');
        } finally {
            setSubmitting(false);
        }
    };

    const renderJobTypeSelection = () => (
        <Box>
            <Typography variant="h6" gutterBottom>
                Select the type of job you want to run
            </Typography>
            <JobTypeSelector selectedType={jobType} onSelect={setJobType} />
        </Box>
    );

    const renderConfiguration = () => (
        <Box>
            <Typography variant="h6" gutterBottom>
                Configure Your {jobType} Job
            </Typography>

            <Grid container spacing={2}>
                <Grid size={{ xs: 12 }}>
                    <TextField
                        fullWidth
                        label="Job Name"
                        name="jobName"
                        value={config.jobName}
                        onChange={handleConfigChange}
                        required
                    />
                </Grid>

                <Grid size={{ xs: 12, sm: 6}}>
                    <TextField
                        fullWidth
                        label="Input Path"
                        name="inputPath"
                        value={config.inputPath}
                        onChange={handleConfigChange}
                        helperText="HDFS path or local path"
                        required
                    />
                </Grid>

                <Grid size={{ xs: 12, sm: 6 }}>
                    <TextField
                        fullWidth
                        label="Output Path"
                        name="outputPath"
                        value={config.outputPath}
                        onChange={handleConfigChange}
                        required
                    />
                </Grid>

                {jobType === 'HADOOP' && (
                    <>
                        <Grid size={{ xs: 12, sm: 6 }}>
                            <TextField
                                fullWidth
                                label="JAR Path"
                                name="jarPath"
                                value={config.jarPath || ''}
                                onChange={handleConfigChange}
                            />
                        </Grid>
                        <Grid size={{ xs: 12, sm: 6 }}>
                            <TextField
                                fullWidth
                                label="Main Class"
                                name="mainClass"
                                value={config.mainClass || ''}
                                onChange={handleConfigChange}
                            />
                        </Grid>
                        <Grid size={{ xs: 12, sm: 6 }}>
                            <TextField
                                fullWidth
                                type="number"
                                label="Memory (MB)"
                                name="memory"
                                value={config.memory || 1024}
                                onChange={handleConfigChange}
                            />
                        </Grid>
                        <Grid size={{ xs: 12, sm: 6 }}>
                            <TextField
                                fullWidth
                                type="number"
                                label="Virtual Cores"
                                name="vCores"
                                value={config.vCores || 1}
                                onChange={handleConfigChange}
                            />
                        </Grid>
                    </>
                )}

                {jobType === 'SPARK' && (
                    <>
                        <Grid size={{ xs: 12 }}>
                            <TextField
                                fullWidth
                                label="Script Path"
                                name="scriptPath"
                                value={config.scriptPath || ''}
                                onChange={handleConfigChange}
                            />
                        </Grid>
                        <Grid size={{ xs: 12, sm: 4 }}>
                            <TextField
                                fullWidth
                                label="Executor Memory"
                                name="executorMemory"
                                value={config.executorMemory || '1g'}
                                onChange={handleConfigChange}
                            />
                        </Grid>
                        <Grid size={{ xs: 12, sm: 4 }}>
                            <TextField
                                fullWidth
                                type="number"
                                label="Executor Cores"
                                name="executorCores"
                                value={config.executorCores || 1}
                                onChange={handleConfigChange}
                            />
                        </Grid>
                        <Grid size={{ xs: 12, sm: 4 }}>
                            <TextField
                                fullWidth
                                type="number"
                                label="Number of Executors"
                                name="numExecutors"
                                value={config.numExecutors || 2}
                                onChange={handleConfigChange}
                            />
                        </Grid>
                    </>
                )}

                {jobType === 'PYTHON' && (
                    <Grid size={{ xs: 12 }}>
                        <TextField
                            fullWidth
                            label="Script Path"
                            name="scriptPath"
                            value={config.scriptPath || ''}
                            onChange={handleConfigChange}
                        />
                    </Grid>
                )}

                {/* Arguments */}
                <Grid size={{ xs: 12 }}>
                    <Typography variant="subtitle1" gutterBottom>
                        Arguments
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1, mb: 1 }}>
                        <TextField
                            size="small"
                            value={newArg}
                            onChange={(e) => setNewArg(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter') {
                                    handleAddArgument();
                                }
                            }}
                            placeholder="Add argument"
                        />
                        <Button
                            variant="outlined"
                            startIcon={<AddIcon />}
                            onClick={handleAddArgument}
                        >
                            Add
                        </Button>
                    </Box>
                    <List>
                        {config.arguments.map((arg, index) => (
                            <ListItem key={index}>
                                <ListItemText primary={arg} />
                                <IconButton onClick={() => handleRemoveArgument(index)} size="small">
                                    <DeleteIcon />
                                </IconButton>
                            </ListItem>
                        ))}
                    </List>
                </Grid>
            </Grid>
        </Box>
    );

    const renderReview = () => (
        <Box>
            <Typography variant="h6" gutterBottom>
                Review Job Configuration
            </Typography>

            <Card>
                <CardContent>
                    <Grid container spacing={2}>
                        <Grid size={{ xs: 6 }}>
                            <Typography variant="body2" color="textSecondary">
                                Job Type
                            </Typography>
                            <Chip label={jobType} color="primary" />
                        </Grid>
                        <Grid size={{ xs: 6 }}>
                            <Typography variant="body2" color="textSecondary">
                                Job Name
                            </Typography>
                            <Typography>{config.jobName}</Typography>
                        </Grid>
                        <Grid size={{ xs: 6 }}>
                            <Typography variant="body2" color="textSecondary">
                                Input Path
                            </Typography>
                            <Typography>{config.inputPath}</Typography>
                        </Grid>
                        <Grid size={{ xs: 6 }}>
                            <Typography variant="body2" color="textSecondary">
                                Output Path
                            </Typography>
                            <Typography>{config.outputPath}</Typography>
                        </Grid>
                        {config.arguments.length > 0 && (
                            <Grid size={{ xs: 12 }}>
                                <Typography variant="body2" color="textSecondary">
                                    Arguments
                                </Typography>
                                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mt: 1 }}>
                                    {config.arguments.map((arg, index) => (
                                        <Chip key={index} label={arg} size="small" />
                                    ))}
                                </Box>
                            </Grid>
                        )}
                    </Grid>
                </CardContent>
            </Card>
        </Box>
    );

    const getStepContent = (step: number) => {
        switch (step) {
            case 0:
                return renderJobTypeSelection();
            case 1:
                return renderConfiguration();
            case 2:
                return renderReview();
            default:
                return 'Unknown step';
        }
    };

    return (
        <Box>
            <Typography variant="h4" gutterBottom>
                Submit New Job
            </Typography>

            {error && (
                <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
                    {error}
                </Alert>
            )}

            <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
                {steps.map((label) => (
                    <Step key={label}>
                        <StepLabel>{label}</StepLabel>
                    </Step>
                ))}
            </Stepper>

            <Box sx={{ mb: 4 }}>
                {getStepContent(activeStep)}
            </Box>

            <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
                <Button
                    disabled={activeStep === 0}
                    onClick={handleBack}
                >
                    Back
                </Button>
                {activeStep === steps.length - 1 ? (
                    <Button
                        variant="contained"
                        startIcon={<SendIcon />}
                        onClick={handleSubmit}
                        disabled={submitting}
                    >
                        {submitting ? 'Submitting...' : 'Submit Job'}
                    </Button>
                ) : (
                    <Button
                        variant="contained"
                        onClick={handleNext}
                        disabled={
                            (activeStep === 0 && !jobType) ||
                            (activeStep === 1 && !config.jobName)
                        }
                    >
                        Next
                    </Button>
                )}
            </Box>
        </Box>
    );
};

export default JobSubmitPage;
