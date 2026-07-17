import React from 'react';
import { useParams } from 'react-router-dom';
import { Box } from '@mui/material';
import JobDetail from '../components/Jobs/JobDetail';

const JobDetailPage: React.FC = () => {
    const { id } = useParams<{ id: string }>();

    return (
        <Box>
            <JobDetail jobId={id} />
        </Box>
    );
};

export default JobDetailPage;
