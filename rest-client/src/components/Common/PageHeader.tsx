import React from 'react';
import { Box, Typography, Button, IconButton, Tooltip } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import AddIcon from '@mui/icons-material/Add';

interface PageHeaderProps {
    title: string;
    subtitle?: string;
    onRefresh?: () => void;
    onAdd?: () => void;
    addLabel?: string;
    children?: React.ReactNode;
}

const PageHeader: React.FC<PageHeaderProps> = (
    {
        title,
        subtitle,
        onRefresh,
        onAdd,
        addLabel = 'Add New',
        children,
    }
) => {
    return (
        <Box sx={{ mb: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems:"center", mb: 1 }}>
                <Box>
                    <Typography variant="h4" component="h1">
                        {title}
                    </Typography>
                    {subtitle && (
                        <Typography variant="body1" color="textSecondary">
                            {subtitle}
                        </Typography>
                    )}
                </Box>
                <Box sx={{ display: 'flex', gap: 1 }}>
                    {onRefresh && (
                        <Tooltip title="Refresh">
                            <IconButton onClick={onRefresh}>
                                <RefreshIcon />
                            </IconButton>
                        </Tooltip>
                    )}
                    {onAdd && (
                        <Button
                            variant="contained"
                            startIcon={<AddIcon />}
                            onClick={onAdd}
                        >
                            {addLabel}
                        </Button>
                    )}
                </Box>
            </Box>
            {children}
        </Box>
    );
};

export default PageHeader;
