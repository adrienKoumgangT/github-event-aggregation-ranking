import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
    Box,
    List,
    ListItem,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    Toolbar,
    Typography,
    Divider,
} from '@mui/material';
import {
    Dashboard as DashboardIcon,
    Apps as AppsIcon,
    Work as WorkIcon,
    Dns as DnsIcon,
    Add as AddIcon,
} from '@mui/icons-material';

interface MenuItem {
    text: string;
    icon: React.ReactElement;
    path: string;
    divider?: boolean;
}

const Sidebar: React.FC = () => {
    const navigate = useNavigate();
    const location = useLocation();

    const menuItems: MenuItem[] = [
        { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
        { text: 'Applications', icon: <AppsIcon />, path: '/applications' },
        { text: 'Jobs', icon: <WorkIcon />, path: '/jobs' },
        { text: 'Submit Job', icon: <AddIcon />, path: '/jobs/submit' },
        { text: 'Nodes', icon: <DnsIcon />, path: '/nodes', divider: true },
    ];

    return (
        <Box>
            <Toolbar>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <DashboardIcon color="primary" />
                    <Typography variant="h6" noWrap component="div" color="primary">
                        YARN Manager
                    </Typography>
                </Box>
            </Toolbar>
            <Divider />
            <List>
                {menuItems.map((item, _index) => (
                    <React.Fragment key={item.text}>
                        <ListItem disablePadding>
                            <ListItemButton
                                selected={location.pathname === item.path}
                                onClick={() => navigate(item.path)}
                            >
                                <ListItemIcon>
                                    {item.icon}
                                </ListItemIcon>
                                <ListItemText primary={item.text} />
                            </ListItemButton>
                        </ListItem>
                        {item.divider && <Divider sx={{ my: 1 }} />}
                    </React.Fragment>
                ))}
            </List>
        </Box>
    );
};

export default Sidebar;
