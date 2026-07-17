import React from 'react';
import { Chip, type ChipProps } from '@mui/material';

interface StatusChipProps {
    status: string | undefined | null;
    size?: ChipProps['size'];
}

const getStatusColor = (status: string | undefined | null): ChipProps['color'] => {
    // Handle undefined/null status
    if (!status) {
        return 'default';
    }

    const upperStatus = status.toUpperCase();

    switch (upperStatus) {
        case 'RUNNING':
        case 'ACTIVE':
        case 'SUBMITTED':
        case 'ACCEPTED':
            return 'info';
        case 'FINISHED':
        case 'COMPLETED':
        case 'HEALTHY':
            return 'success';
        case 'FAILED':
        case 'ERROR':
        case 'UNHEALTHY':
        case 'LOST':
            return 'error';
        case 'KILLED':
        case 'CANCELLED':
            return 'warning';
        case 'PENDING':
        case 'NEW':
        case 'NEW_SAVING':
            return 'default';
        case 'DECOMMISSIONED':
            return 'secondary';
        default:
            return 'default';
    }
};

const StatusChip: React.FC<StatusChipProps> = ({ status, size = 'small' }) => {
    return (
        <Chip
            label={status || 'UNKNOWN'}
            color={getStatusColor(status)}
            size={size}
            variant="filled"
        />
    );
};

export default StatusChip;
