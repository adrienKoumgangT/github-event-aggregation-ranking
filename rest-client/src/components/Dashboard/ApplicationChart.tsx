import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';
import {
    PieChart,
    Pie,
    Cell,
    ResponsiveContainer,
    Tooltip,
    Legend,
} from 'recharts';
import { type ClusterMetrics } from '../../types/cluster';

interface ApplicationChartProps {
    metrics: ClusterMetrics | null;
}

const COLORS = ['#1976d2', '#2e7d32', '#ed6c02', '#d32f2f', '#9c27b0', '#757575'];

const ApplicationChart: React.FC<ApplicationChartProps> = ({ metrics }) => {
    if (!metrics) return null;

    const data = [
        { name: 'Running', value: metrics.appsRunning },
        { name: 'Completed', value: metrics.appsCompleted },
        { name: 'Pending', value: metrics.appsPending },
        { name: 'Failed', value: metrics.appsFailed },
        { name: 'Killed', value: metrics.appsKilled },
        // { name: 'Submitted', value: metrics.appsSubmitted },
    ].filter(item => item.value > 0);

    return (
        <Card>
            <CardContent>
                <Typography variant="h6" gutterBottom>
                    Application Status Distribution
                </Typography>
                <Box sx={{ width: '100%', height: 300 }}>
                    <ResponsiveContainer>
                        <PieChart>
                            <Pie
                                data={data}
                                cx="50%"
                                cy="50%"
                                labelLine={false}
                                outerRadius={80}
                                fill="#8884d8"
                                dataKey="value"
                                label={({ name, percent }) =>
                                    `${name} ${(percent).toFixed(0)}%`
                                }
                            >
                                {data.map((_entry, index) => (
                                    <Cell
                                        key={`cell-${index}`}
                                        fill={COLORS[index % COLORS.length]}
                                    />
                                ))}
                            </Pie>
                            <Tooltip />
                            <Legend />
                        </PieChart>
                    </ResponsiveContainer>
                </Box>
            </CardContent>
        </Card>
    );
};

export default ApplicationChart;
