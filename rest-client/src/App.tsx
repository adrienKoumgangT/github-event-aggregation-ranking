import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { theme } from './theme';
import AppLayout from './components/Layout/AppLayout';
import DashboardPage from './pages/DashboardPage';
import ApplicationsPage from './pages/ApplicationsPage';
import ApplicationDetailPage from './pages/ApplicationDetailPage';
import JobsPage from './pages/JobsPage';
import JobSubmitPage from './pages/JobSubmitPage';
import JobDetailPage from './pages/JobDetailPage';
import NodesPage from './pages/NodesPage';

const App: React.FC = () => {
  return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <AppLayout>
            <Routes>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/applications" element={<ApplicationsPage />} />
              <Route path="/applications/:id" element={<ApplicationDetailPage />} />
              <Route path="/jobs" element={<JobsPage />} />
              <Route path="/jobs/submit" element={<JobSubmitPage />} />
              <Route path="/jobs/:id" element={<JobDetailPage />} />
              <Route path="/nodes" element={<NodesPage />} />
            </Routes>
          </AppLayout>
        </Router>
      </ThemeProvider>
  );
};

export default App;
