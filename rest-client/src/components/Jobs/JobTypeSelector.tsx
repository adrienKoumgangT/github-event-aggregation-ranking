import React from 'react';
import {
    Card,
    CardContent,
    Typography,
    Grid,
    Box,
    Chip,
} from '@mui/material';
import {
    Storage as HadoopIcon,
    Analytics as SparkIcon,
    Code as PythonIcon,
} from '@mui/icons-material';
import { type JobType } from '../../types/job';

interface JobTypeSelectorProps {
    selectedType: JobType | null;
    onSelect: (type: JobType) => void;
}

const jobTypes = [
    {
        type: 'HADOOP' as JobType,
        name: 'Hadoop MapReduce',
        description: 'Distributed processing of large data sets across clusters',
        icon: <HadoopIcon sx={{ fontSize: 40 }} />,
        color: '#1976d2',
    },
    {
        type: 'SPARK' as JobType,
        name: 'Apache Spark',
        description: 'Fast and general engine for large-scale data processing',
        icon: <SparkIcon sx={{ fontSize: 40 }} />,
        color: '#e37400',
    },
    {
        type: 'PYTHON' as JobType,
        name: 'Python Script',
        description: 'Run standalone Python data processing scripts',
        icon: <PythonIcon sx={{ fontSize: 40 }} />,
        color: '#3776ab',
    },
];

const JobTypeSelector: React.FC<JobTypeSelectorProps> = ({
                                                             selectedType,
                                                             onSelect,
                                                         }) => {
    return (
        <Grid container spacing={3}>
            {jobTypes.map((jobType) => (
                <Grid size={{ xs: 12, sm: 6, md: 4 }} key={jobType.type}>
                    <Card
                        sx={{
                            cursor: 'pointer',
                            border: selectedType === jobType.type ? 2 : 1,
                            borderColor: selectedType === jobType.type ? jobType.color : 'divider',
                            '&:hover': {
                                borderColor: jobType.color,
                                boxShadow: 3,
                            },
                        }}
                        onClick={() => onSelect(jobType.type)}
                    >
                        <CardContent>
                            <Box sx={{ display: 'flex', alignItems: 'center', flexDirection: 'column', gap: 2 }}>
                                <Box sx={{ color: jobType.color }}>
                                    {jobType.icon}
                                </Box>
                                <Typography variant="h6" align="center">
                                    {jobType.name}
                                </Typography>
                                <Typography
                                    variant="body2"
                                    color="textSecondary"
                                    align="center"
                                >
                                    {jobType.description}
                                </Typography>
                                {selectedType === jobType.type && (
                                    <Chip
                                        label="Selected"
                                        size="small"
                                        sx={{ backgroundColor: jobType.color, color: 'white' }}
                                    />
                                )}
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>
            ))}
        </Grid>
    );
};

export default JobTypeSelector;
