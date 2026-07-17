import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';

interface LoadingSpinnerProps {
    message?: string;
    fullScreen?: boolean;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = (
    {
        message = 'Loading...',
        fullScreen = false,
    }
) => {
    return (
        <Box
            sx={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                minHeight: fullScreen ? '100vh' : '200px',
            }}
        >
            <CircularProgress size={40} />
            {message && (
                <Typography variant="body1" color="textSecondary" sx={{ mt: 2 }}>
                    {message}
                </Typography>
            )}
        </Box>
    );
};

export default LoadingSpinner;
