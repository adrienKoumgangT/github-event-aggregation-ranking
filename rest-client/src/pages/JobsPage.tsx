import React from 'react';
import { Box } from '@mui/material';
import JobList from '../components/Jobs/JobList';

const JobsPage: React.FC = () => {
    return (
        <Box>
            <JobList />
        </Box>
    );
};

export default JobsPage;
