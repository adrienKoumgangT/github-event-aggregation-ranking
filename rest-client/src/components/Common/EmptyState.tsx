import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import InboxIcon from '@mui/icons-material/Inbox';

interface EmptyStateProps {
    title?: string;
    message?: string;
    action?: {
        label: string;
        onClick: () => void;
    };
    icon?: React.ReactElement;
}

const EmptyState: React.FC<EmptyStateProps> = (
    {
        title = 'No Data',
        message = 'There is nothing to display here.',
        action,
        icon,
    }
) => {
    return (
        <Box
            sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                py: 8,
                px: 2,
            }}
        >
            <Box sx={{ color: 'text.disabled', mb: 2 }}>
                {icon || <InboxIcon sx={{ fontSize: 64 }} />}
            </Box>
            <Typography variant="h6" color="textSecondary" gutterBottom>
                {title}
            </Typography>
            <Typography
                variant="body2"
                color="textSecondary"
                align="center"
                sx={{ mb: 3 }}
            >
                {message}
            </Typography>
            {action && (
                <Button variant="contained" onClick={action.onClick}>
                    {action.label}
                </Button>
            )}
        </Box>
    );
};

export default EmptyState;
