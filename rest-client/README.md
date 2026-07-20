# YARN Cluster Management - REST Client

A React-based web frontend for managing Hadoop YARN clusters. 
This application provides a user-friendly interface for monitoring cluster resources, managing applications, submitting jobs, and tracking node health.


## Features

### Dashboard
- Real-time cluster metrics overview
- Application status distribution charts
- Memory and vCore resource usage graphs
- Node health status monitoring
- Auto-refreshing data with configurable intervals

### Applications Management
- View all YARN applications with filtering
- Search by application ID, name, or user
- Filter by application state
- Detailed application information view
- Kill running applications
- Application progress tracking

### Job Submission
- Multi-step job submission wizard
- Support for Hadoop MapReduce, Apache Spark, and Python jobs
- Dynamic configuration forms per job type
- Argument management with add/remove functionality
- Job configuration review before submission

### Job Management
- List all submitted jobs with filtering
- Filter by job status and type
- Real-time job progress monitoring
- View detailed job logs with filtering
- Kill running jobs
- Download job logs
- Delete completed jobs

### Node Monitoring
- View all cluster nodes
- Filter by node state and rack
- Node resource utilization visualization
- Memory and vCore usage progress bars
- Node health status indicators
- Detailed node information dialog

## Tech Stack

| Technology | Version | Description |
|------------|---------|-------------|
| React | 19.x | UI Framework |
| TypeScript | 6.x | Type Safety |
| Vite | 8.x | Build Tool |
| Material-UI (MUI) | 9.x | Component Library |
| React Router | 7.x | Routing |
| Axios | 1.x | HTTP Client |
| Recharts | 3.x | Charts & Graphs |
| Emotion | 11.x | CSS-in-JS |

## Prerequisites

- Node.js 18.x or higher
- npm 9.x or higher (or yarn/pnpm)
- Running YARN REST Server (backend)

## Installation

### 1. Navigate to the frontend directory

```bash
cd rest-client
```

### 2. Install dependencies

```bash
npm install
```

### 3. Configure environment variables

```bash
# Create .env file from example
cp .env.example .env
```

### 4. Start the development server

```bash
npm run dev
```

The application will be available at `http://localhost:3000` (or `http://localhost:5173` by default).

## Configuration

### Environment Variables (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `http://localhost:5000/api` |

### Vite Configuration (vite.config.ts)

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      }
    }
  }
})
```

### Proxy Setup

When using the Vite proxy (recommended for development):
- All `/api/*` requests are forwarded to the Flask backend
- No CORS issues during development
- Frontend uses relative URLs for API calls

```typescript
// api.ts - When using proxy
const API_BASE_URL = '/api';

// api.ts - When using direct connection
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';
```

## Running the Application

### Development Mode

```bash
# Start development server with hot reload
npm run dev
```

### Production Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Lint

```bash
# Run linter
npm run lint
```


## Pages & Components

### Dashboard Page (`/`)
- **ClusterOverview**: Cards showing active nodes, running apps, memory, vCores
- **ApplicationChart**: Pie chart of application status distribution
- **ResourceUsage**: Bar charts for memory and vCore usage
- **NodeHealth**: Health status summary of all nodes

### Applications Page (`/applications`)
- **ApplicationList**: Table with search, status filter, and pagination
- **ApplicationDetail** (`/applications/:id`): Detailed view with progress, resources, timing

### Jobs Page (`/jobs`)
- **JobList**: Table with search, status/type filters, and pagination
- **JobSubmit** (`/jobs/submit`): Multi-step wizard for job submission
- **JobDetail** (`/jobs/:id`): Job status, progress, configuration, and logs

### Nodes Page (`/nodes`)
- **NodeList**: Grid of node cards with resource utilization bars
- **NodeDetail** (`/nodes/:id`): Detailed node view with utilization charts

## API Integration

### Service Layer

Each service file handles API calls for a specific domain:

```typescript
// services/clusterService.ts
import api from './api';

export const clusterService = {
  getMetrics: () => api.get('/cluster/metrics'),
  getInfo: () => api.get('/cluster/info'),
  getScheduler: () => api.get('/cluster/scheduler'),
};

// Usage in components
const metrics = await clusterService.getMetrics();
```

### Axios Configuration

- Base URL from environment variable or Vite proxy
- Request interceptor for auth tokens
- Response interceptor for error handling
- Automatic error formatting

### Custom Hooks

```typescript
// useApi.ts - Generic API call hook
const { data, loading, error, execute } = useApi(clusterService.getMetrics);

// usePolling.ts - Auto-refresh data
usePolling(fetchData, 5000); // Poll every 5 seconds

// useJobStatus.ts - Job-specific polling
const { job, loading, error, isRunning } = useJobStatus(jobId);
```

## State Management

### AppContext

Global application state for:
- Auto-refresh settings
- Refresh interval configuration
- Dark mode toggle
- Cluster URL configuration

```typescript
import { useAppContext } from '../context/AppContext';

const { autoRefresh, refreshInterval, toggleDarkMode } = useAppContext();
```

### Component State

- Local state for component-specific data
- API data cached in component state
- Polling for real-time updates on running resources

## Styling

### Material-UI v9

The application uses MUI v9 with the following key changes from v5:
- `sx` prop for all styling (no direct style props)
- `size` prop instead of `xs`/`md` on Grid
- `slotProps` instead of `InputProps`

### Theme

Custom theme configuration in `theme.ts`:
- Primary and secondary color palettes
- Typography customization
- Component style overrides (Card, Button)

### Responsive Design

- Mobile-first approach
- Drawer navigation collapses on small screens
- Cards and tables responsive across breakpoints

## Building for Production

```bash
# Build the application
npm run build

# Output is in the dist/ directory
```

The production build:
- Minifies JavaScript and CSS
- Optimizes assets
- Generates static files for deployment

## Docker Deployment

### Build the Image

```bash
docker build -t yarn-rest-client .
```

### Run the Container

```bash
docker run -d \
  -p 80:80 \
  -e VITE_API_URL=http://backend:5000/api \
  --name yarn-rest-client \
  yarn-rest-client
```

### Docker Compose

```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    environment:
      - VITE_API_URL=http://backend:5000/api
    depends_on:
      - backend
```

### Nginx Configuration

Production deployment uses Nginx to serve static files and proxy API requests:

```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Development Guide

### Adding a New Page

1. Create component in `src/components/<Feature>/`
2. Create page in `src/pages/`
3. Add route in `src/App.tsx`
4. Add navigation item in `src/components/Layout/Sidebar.tsx`
5. Add API service method if needed

### Adding a New Feature

1. Define types in `src/types/`
2. Create API service in `src/services/`
3. Build components in `src/components/`
4. Create page in `src/pages/`
5. Add to navigation and routes

### TypeScript Guidelines

- Always define interfaces for props
- Use type definitions for API responses
- Avoid `any` - use proper types
- Export types from dedicated files in `src/types/`

### Component Patterns

```typescript
// Functional component with TypeScript
interface MyComponentProps {
  title: string;
  onAction: () => void;
}

const MyComponent: React.FC<MyComponentProps> = ({ title, onAction }) => {
  return <div>{title}</div>;
};
```

## Troubleshooting

### Common Issues

**1. Blank Page**
- Check browser console for errors
- Verify `@emotion/react` and `@emotion/styled` are installed
- Check `main.tsx` is the correct entry point (delete `index.tsx`)

**2. CORS Errors**
- Ensure backend has CORS enabled
- Use Vite proxy for development (configured in `vite.config.ts`)
- Check API URL in `.env` file

**3. API Connection Refused**
- Verify backend server is running
- Check port configuration
- Test API directly: `curl http://localhost:5000/api/cluster/info`

**4. TypeScript Errors**
- Run `npm run lint` to check for errors
- Ensure all type definitions are correct
- Check MUI v9 syntax (use `sx` prop, `size` on Grid)

**5. Build Errors**
```bash
# Clear cache and rebuild
rm -rf node_modules dist
npm install
npm run build
```

**6. Port Already in Use**
```bash
# Change port in vite.config.ts
server: {
  port: 3001
}

# Or kill existing process
lsof -ti:3000 | xargs kill -9
```

### Debug Mode

- Open browser DevTools (F12)
- Check Console tab for JavaScript errors
- Check Network tab for API request status
- React DevTools extension for component inspection

## Performance

- Code splitting with React.lazy()
- Memoized components with React.memo()
- Debounced search inputs
- Pagination for large datasets
- Optimized re-renders with proper hooks usage

## License

This project is part of the GitHub Event Aggregation Ranking system.

