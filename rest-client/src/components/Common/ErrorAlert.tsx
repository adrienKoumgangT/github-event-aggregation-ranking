import React from 'react';
import { Alert, AlertTitle, Box, Button } from '@mui/material';

interface ErrorAlertProps {
    title?: string;
    message: string;
    onRetry?: () => void;
    onDismiss?: () => void;
}

const ErrorAlert: React.FC<ErrorAlertProps> = (
    {
        title = 'Error',
        message,
        onRetry,
        onDismiss,
    }
) => {
    return (
        <Box sx={{ my: 2 }}>
            <Alert
                severity="error"
                action={
                    <Box>
                        {onRetry && (
                            <Button color="inherit" size="small" onClick={onRetry} sx={{ mr: 1 }}>
                                Retry
                            </Button>
                        )}
                        {onDismiss && (
                            <Button color="inherit" size="small" onClick={onDismiss}>
                                Dismiss
                            </Button>
                        )}
                    </Box>
                }
            >
                <AlertTitle>{title}</AlertTitle>
                {message}
            </Alert>
        </Box>
    );
};

export default ErrorAlert;
