import React from 'react';
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogContentText,
    DialogActions,
    Button,
} from '@mui/material';

interface ConfirmDialogProps {
    open: boolean;
    title: string;
    message: string;
    confirmText?: string;
    cancelText?: string;
    onConfirm: () => void;
    onCancel: () => void;
    severity?: 'error' | 'warning' | 'info';
}

const ConfirmDialog: React.FC<ConfirmDialogProps> = (
    {
        open,
        title,
        message,
        confirmText = 'Confirm',
        cancelText = 'Cancel',
        onConfirm,
        onCancel,
        severity = 'warning',
    }
) => {
    const getConfirmColor = () => {
        switch (severity) {
            case 'error':
                return 'error';
            case 'warning':
                return 'warning';
            case 'info':
                return 'primary';
            default:
                return 'primary';
        }
    };

    return (
        <Dialog open={open} onClose={onCancel} maxWidth="sm" fullWidth>
            <DialogTitle>{title}</DialogTitle>
            <DialogContent>
                <DialogContentText>{message}</DialogContentText>
            </DialogContent>
            <DialogActions>
                <Button onClick={onCancel} color="inherit">
                    {cancelText}
                </Button>
                <Button onClick={onConfirm} color={getConfirmColor()} variant="contained">
                    {confirmText}
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default ConfirmDialog;
