import React from 'react';
import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    TablePagination,
    Typography,
    Box,
} from '@mui/material';

interface Column {
    id: string;
    label: string;
    minWidth?: number;
    align?: 'left' | 'right' | 'center';
    format?: (value: any, row: any) => React.ReactNode;
}

interface DataTableProps {
    columns: Column[];
    rows: any[];
    title?: string;
    rowsPerPageOptions?: number[];
    defaultRowsPerPage?: number;
    onRowClick?: (row: any) => void;
}

const DataTable: React.FC<DataTableProps> = (
    {
        columns,
        rows,
        title,
        rowsPerPageOptions = [10, 25, 50, 100],
        defaultRowsPerPage = 10,
        onRowClick,
    }
) => {
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(defaultRowsPerPage);

    const handleChangePage = (_event: unknown, newPage: number) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
        setRowsPerPage(+event.target.value);
        setPage(0);
    };

    const currentRows = rows.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);

    return (
        <Paper sx={{ width: '100%', overflow: 'hidden' }}>
            {title && (
                <Box sx={{ p: 2 }}>
                    <Typography variant="h6">{title}</Typography>
                </Box>
            )}
            <TableContainer sx={{ maxHeight: 440 }}>
                <Table stickyHeader>
                    <TableHead>
                        <TableRow>
                            {columns.map((column) => (
                                <TableCell
                                    key={column.id}
                                    align={column.align}
                                    style={{ minWidth: column.minWidth }}
                                >
                                    <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
                                        {column.label}
                                    </Typography>
                                </TableCell>
                            ))}
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {currentRows.map((row, index) => (
                            <TableRow
                                hover
                                role="checkbox"
                                tabIndex={-1}
                                key={row.id || index}
                                onClick={() => onRowClick?.(row)}
                                sx={{ cursor: onRowClick ? 'pointer' : 'default' }}
                            >
                                {columns.map((column) => {
                                    const value = row[column.id];
                                    return (
                                        <TableCell key={column.id} align={column.align}>
                                            {column.format ? column.format(value, row) : value}
                                        </TableCell>
                                    );
                                })}
                            </TableRow>
                        ))}
                        {currentRows.length === 0 && (
                            <TableRow>
                                <TableCell colSpan={columns.length} align="center">
                                    <Typography variant="body2" color="textSecondary">
                                        No data available
                                    </Typography>
                                </TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </TableContainer>
            <TablePagination
                rowsPerPageOptions={rowsPerPageOptions}
                component="div"
                count={rows.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
            />
        </Paper>
    );
};

export default DataTable;
