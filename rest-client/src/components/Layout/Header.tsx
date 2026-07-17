import React from 'react';
import { Box, Typography, IconButton, Chip } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import { useLocation } from 'react-router-dom';

interface HeaderProps {
    onRefresh?: () => void;
}

const Header: React.FC<HeaderProps> = ({ onRefresh }) => {
    const location = useLocation();

    const getPageTitle = (): string => {
        const path = location.pathname;
        if (path === '/') return 'Dashboard';
        if (path.startsWith('/applications/')) return 'Application Details';
        if (path === '/applications') return 'Applications';
        if (path.startsWith('/jobs/submit')) return 'Submit Job';
        if (path.startsWith('/jobs/')) return 'Job Details';
        if (path === '/jobs') return 'Jobs';
        if (path.startsWith('/nodes/')) return 'Node Details';
        if (path === '/nodes') return 'Nodes';
        return 'YARN Cluster Management';
    };

    return (
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Typography variant="h6" noWrap component="div">
                    {getPageTitle()}
                </Typography>
                <Chip
                    label="v1.0.0"
                    size="small"
                    color="primary"
                    variant="outlined"
                />
            </Box>
            <Box>
                {onRefresh && (
                    <IconButton color="inherit" onClick={onRefresh}>
                        <RefreshIcon />
                    </IconButton>
                )}
            </Box>
        </Box>
    );
};

export default Header;
