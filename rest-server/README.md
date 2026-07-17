# YARN Cluster Management - REST Server

A Flask-based REST API server that acts as an intermediate layer between the client interface and the Hadoop YARN distributed backend. 
This server provides a unified API for managing Hadoop/Spark jobs, monitoring cluster resources, and tracking applications on a YARN cluster.


## Features

- **Cluster Management**: Monitor cluster information, metrics, and scheduler configuration
- **Application Management**: View, submit, and kill YARN applications
- **Job Submission**: Submit Hadoop MapReduce, Apache Spark, and Python jobs
- **Node Monitoring**: Track node health, resource utilization, and statistics
- **RESTful API**: Full REST API with Flask-RESTX
- **Swagger Documentation**: Interactive API documentation available at `/docs`
- **SQLite Database**: Persistent storage for job configurations and logs
- **CORS Support**: Cross-Origin Resource Sharing enabled for web clients
- **Logging**: Comprehensive logging with rotating file handlers

## Architecture

```
┌──────────────────┐     ┌─────────────────┐
│                  │     │                 │
│  Flask REST API  │────▶│  YARN Cluster   │
│  (localhost:5000)│     │  (RM REST API)  │
│                  │     │                 │
└──────────────────┘     └─────────────────┘
          │
          ▼
    ┌──────────────┐
    │   SQLite DB  │
    │  (jobs.db)   │
    └──────────────┘
```

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Access to a Hadoop YARN cluster with REST API enabled
- Virtual environment (recommended)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd github-event-aggregation-ranking/rest-server
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

### Environment Variables (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Server host address | `0.0.0.0` |
| `PORT` | Server port | `5000` |
| `DEBUG` | Debug mode | `false` |
| `YARN_RM_HOST` | YARN ResourceManager host | `10.1.1.144` |
| `YARN_RM_PORT` | YARN ResourceManager port | `8088` |
| `DATABASE_URL` | SQLite database URL | `sqlite:///data/jobs.db` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `HADOOP_HOME` | Hadoop installation path | `/opt/hadoop` |
| `SPARK_HOME` | Spark installation path | `/opt/spark` |
| `MAX_CONCURRENT_JOBS` | Maximum concurrent jobs | `5` |
| `JOB_TIMEOUT_SECONDS` | Job timeout in seconds | `3600` |

### Configuration File

The server uses `config/settings.py` which reads from environment variables and provides default values.

## Running the Server

### Development Mode

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the server
python src/app.py
```

### Using Flask CLI

```bash
# Set Flask app environment variable
export FLASK_APP=src/app.py
export FLASK_ENV=development

# Run with Flask CLI
flask run --host=0.0.0.0 --port=5000
```

### Production Mode

```bash
# Using gunicorn (install first: pip install gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 src.app:create_app()
```

## API Documentation

### Swagger UI

Once the server is running, access the interactive API documentation at:

```
http://localhost:5000/docs
```

### API Base URL

```
http://localhost:5000/api
```

## API Endpoints

### Cluster Information

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/cluster/info` | Get cluster information |
| GET | `/api/cluster/metrics` | Get cluster metrics |
| GET | `/api/cluster/scheduler` | Get scheduler information |

### Applications

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/applications/` | List all applications |
| GET | `/api/applications/{id}` | Get application details |
| GET | `/api/applications/{id}/state` | Get application state |
| PUT | `/api/applications/{id}/state` | Kill an application |
| GET | `/api/applications/statistics` | Get application statistics |
| POST | `/api/applications/submit` | Submit new application |

### Jobs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/jobs/` | List all jobs (with filters) |
| GET | `/api/jobs/types` | Get available job types |
| POST | `/api/jobs/submit` | Submit a new job |
| GET | `/api/jobs/{id}` | Get job status |
| GET | `/api/jobs/{id}/result` | Get job results |
| PUT | `/api/jobs/{id}/kill` | Kill a running job |
| GET | `/api/jobs/{id}/logs` | Get job logs |
| DELETE | `/api/jobs/{id}` | Delete a job |
| GET | `/api/jobs/statistics` | Get job statistics |

**Query Parameters for GET /jobs/:**
- `status` - Filter by status (PENDING, RUNNING, FINISHED, FAILED, KILLED)
- `type` - Filter by type (HADOOP, SPARK, PYTHON)
- `user` - Filter by user
- `limit` - Number of results (default: 100)
- `offset` - Pagination offset (default: 0)

### Nodes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/nodes/` | List all nodes (with filters) |
| GET | `/api/nodes/{id}` | Get node details |
| GET | `/api/nodes/{id}/utilization` | Get node resource utilization |
| GET | `/api/nodes/statistics` | Get node statistics |
| GET | `/api/nodes/health` | Get node health status |

**Query Parameters for GET /nodes/:**
- `state` - Filter by node state (RUNNING, UNHEALTHY, etc.)
- `rack` - Filter by rack name

### Example Requests

```bash
# Get cluster metrics
curl -X GET http://localhost:5000/api/cluster/metrics

# List running applications
curl -X GET http://localhost:5000/api/applications/

# Submit a Spark job
curl -X POST http://localhost:5000/api/jobs/submit \
  -H "Content-Type: application/json" \
  -d '{
    "type": "SPARK",
    "configuration": {
      "jobName": "word-count",
      "scriptPath": "/path/to/script.py",
      "inputPath": "/input/data",
      "outputPath": "/output/result",
      "executorMemory": "1g",
      "executorCores": 2,
      "numExecutors": 3
    }
  }'

# Get jobs with filters
curl -X GET "http://localhost:5000/api/jobs/?status=RUNNING&type=SPARK&limit=10"
```


## Database

The server uses SQLite for persistent storage of job information.

### Database Location

```
data/jobs.db
```

### Tables

- **jobs**: Job metadata (ID, name, type, status, timestamps, etc.)
- **job_configurations**: Job configuration details (paths, resources, arguments)
- **job_logs**: Job execution logs (timestamps, levels, messages)

### Database Operations

The database is automatically created when the server starts. It uses SQLAlchemy ORM with Flask-SQLAlchemy extension.

```python
# Example: Query jobs from database
from database.repository import JobRepository

# Get all running jobs
jobs = JobRepository.get_all_jobs(status='RUNNING')

# Get job by ID
job = JobRepository.get_job('job-uuid')

# Add log entry
JobRepository.add_job_log('job-uuid', 'Job started', 'INFO')
```

## Logging

### Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General operational messages
- **WARNING**: Warning conditions
- **ERROR**: Error conditions
- **CRITICAL**: Critical conditions

### Log Files

- **Console**: Real-time logs during development
- **logs/app.log**: All application logs (rotates at 10MB, keeps 5 backups)
- **logs/error.log**: Error-level logs only

### Viewing Logs

```bash
# View application logs in real-time
tail -f logs/app.log

# View error logs
tail -f logs/error.log

# Search for specific patterns
grep "ERROR" logs/app.log
grep "YARN" logs/app.log
```

## Development

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_cluster.py

# Run with coverage
python -m pytest --cov=src tests/
```


### Creating New Endpoints

1. Create models in `namespaces/<name>/models.py`
2. Create service in `namespaces/<name>/service.py`
3. Create routes in `namespaces/<name>/namespace.py`
4. Register namespace in `app.py`

## Docker Deployment

### Build the Image

```bash
docker build -t yarn-rest-server .
```

### Run the Container

```bash
docker run -d \
  -p 5000:5000 \
  -e YARN_RM_HOST=10.1.1.144 \
  -e YARN_RM_PORT=8088 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  --name yarn-rest-server \
  yarn-rest-server
```

### Using Docker Compose

```yaml
version: '3.8'
services:
  backend:
    build: ./rest-server
    ports:
      - "5000:5000"
    environment:
      - YARN_RM_HOST=10.1.1.144
      - YARN_RM_PORT=8088
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
```

## Troubleshooting

### Common Issues

**1. CORS Errors**
- Ensure Flask-CORS is installed: `pip install flask-cors`
- Check CORS configuration in `app.py`
- Use Vite proxy for frontend development

**2. Database Errors**
- Ensure `data/` directory exists and is writable
- Check database URL in `.env` file
- Delete `data/jobs.db` to recreate the database

**3. YARN Connection Issues**
- Verify YARN ResourceManager is running
- Check `YARN_RM_HOST` and `YARN_RM_PORT` in `.env`
- Test YARN API directly: `curl http://<YARN_RM_HOST>:<YARN_RM_PORT>/ws/cluster/info`

**4. Port Already in Use**
```bash
# Find process using port 5000
lsof -i :5000
# Kill the process
kill -9 <PID>
```

### Debug Mode

Enable debug mode for more detailed error messages:

```bash
# In .env file
DEBUG=true
```

Or set environment variable:
```bash
export DEBUG=true
python src/app.py
```

## License

This project is part of the GitHub Event Aggregation Ranking system.

