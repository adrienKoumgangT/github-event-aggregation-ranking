import React from 'react';
import { Chip, Tooltip } from '@mui/material';
import {
    FiberNew as NewIcon,
    Save as SavingIcon,
    Send as SubmittedIcon,
    CheckCircle as AcceptedIcon,
    PlayArrow as RunningIcon,
    Done as FinishedIcon,
    Error as FailedIcon,
    Cancel as KilledIcon,
} from '@mui/icons-material';
import type { ApplicationState } from '../../types/application';

interface ApplicationStateBadgeProps {
    state: ApplicationState;
    size?: 'small' | 'medium';
    showIcon?: boolean;
}

const stateConfig: Record<
    ApplicationState,
    { color: string; label: string; icon: React.ReactElement; description: string }
> = {
    NEW: {
        color: '#757575',
        label: 'New',
        icon: <NewIcon sx={{ fontSize: 16 }} />,
        description: 'Application has been created',
    },
    NEW_SAVING: {
        color: '#616161',
        label: 'New Saving',
        icon: <SavingIcon sx={{ fontSize: 16 }} />,
        description: 'Application is being saved',
    },
    SUBMITTED: {
        color: '#1976d2',
        label: 'Submitted',
        icon: <SubmittedIcon sx={{ fontSize: 16 }} />,
        description: 'Application has been submitted',
    },
    ACCEPTED: {
        color: '#388e3c',
        label: 'Accepted',
        icon: <AcceptedIcon sx={{ fontSize: 16 }} />,
        description: 'Application has been accepted by the scheduler',
    },
    RUNNING: {
        color: '#2e7d32',
        label: 'Running',
        icon: <RunningIcon sx={{ fontSize: 16 }} />,
        description: 'Application is currently running',
    },
    FINISHED: {
        color: '#1b5e20',
        label: 'Finished',
        icon: <FinishedIcon sx={{ fontSize: 16 }} />,
        description: 'Application completed successfully',
    },
    FAILED: {
        color: '#d32f2f',
        label: 'Failed',
        icon: <FailedIcon sx={{ fontSize: 16 }} />,
        description: 'Application failed to complete',
    },
    KILLED: {
        color: '#e65100',
        label: 'Killed',
        icon: <KilledIcon sx={{ fontSize: 16 }} />,
        description: 'Application was killed by user or admin',
    },
};

const ApplicationStateBadge: React.FC<ApplicationStateBadgeProps> = (
    {
        state,
        size = 'small',
        showIcon = true,
    }
) => {
    const config = stateConfig[state] || {
        color: '#757575',
        label: state,
        icon: <NewIcon sx={{ fontSize: 16 }} />,
        description: `State: ${state}`,
    };

    return (
        <Tooltip title={config.description} arrow>
            <Chip
                icon={showIcon ? config.icon : undefined}
                label={config.label}
                size={size}
                sx={{
                    backgroundColor: config.color,
                    color: 'white',
                    fontWeight: 500,
                    '& .MuiChip-icon': {
                        color: 'white',
                    },
                }}
            />
        </Tooltip>
    );
};

export default ApplicationStateBadge;
