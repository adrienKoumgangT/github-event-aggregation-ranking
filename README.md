# GitHub Event Aggregation Ranking

A distributed analytics system for processing and ranking GitHub Archive events using multiple approaches: Hadoop MapReduce, Apache Spark, and Python (non-parallel).
The system includes a REST API server and a React web client for job submission and cluster monitoring.

## Overview

This project implements three different approaches to process GitHub Archive events:

| Implementation | Type | Processing | Best For |
|---------------|------|------------|----------|
| Hadoop MapReduce | Java | Distributed (2 jobs) | Large batch processing |
| Apache Spark | Python/PySpark | Distributed (in-memory) | Fast iterative processing |
| Python Non-Parallel | Python | Sequential | Small datasets, comparison |

Each implementation:
1. **Counts events** per repository, date, and event type
2. **Ranks top N events** per date across all repositories

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    React Web Client                          │
│                  (http://localhost:3000)                     │
│  ┌───────────┐  ┌────────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Dashboard │  │Applications│  │  Jobs    │  │  Nodes   │   │
│  └───────────┘  └────────────┘  └──────────┘  └──────────┘   │
└───────────────────────┬──────────────────────────────────────┘
                        │ REST API
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  Flask REST API Server                      │
│                  (http://localhost:5000)                    │
│  ┌──────────┐  ┌────────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Cluster  │  │Applications│  │   Jobs   │  │  Nodes   │   │
│  │   API    │  │    API     │  │    API   │  │   API    │   │
│  └──────────┘  └────────────┘  └──────────┘  └──────────┘   │
│                        │                                    │
│                  ┌─────┴─────┐                              │
│                  │  SQLite DB │                             │
│                  └───────────┘                              │
└───────────────────────┬─────────────────────────────────────┘
                        │ YARN REST API
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   Hadoop YARN Cluster                       │
│  ┌───────────┐  ┌──────────┐  ┌──────────┐                  │
│  │ResourceMgr│  │ NodeMgr 1│  │ NodeMgr 2│  ...             │
│  └───────────┘  └──────────┘  └──────────┘                  │
│  ┌──────────────────────────────────────────┐               │
│  │              HDFS Storage                │               │
│  └──────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
github-event-aggregation-ranking/
├── hadoop/                          # Hadoop MapReduce implementation
│   ├── src/main/java/it/unipi/
│   │   ├── App.java                 # Main driver (2 MapReduce jobs)
│   │   ├── EventCountMapper.java    # Job 1 Mapper
│   │   ├── EventCountReducer.java   # Job 1 Reducer/Combiner
│   │   ├── TopEventsMapper.java     # Job 2 Mapper
│   │   └── TopEventsReducer.java    # Job 2 Reducer
│   ├── pom.xml                      # Maven configuration
│   ├── target/
│   │   └── hadoop-1.0-SNAPSHOT.jar  # Built JAR
│   └── README.md
│
├── spark/                           # Apache Spark implementation
│   ├── main.py                      # PySpark script
│   └── README.md
│
├── python-non-parallel/             # Python sequential implementation
│   ├── main.py                      # Python script
│   └── README.md
│
├── rest-server/                     # Flask REST API server
│   ├── src/
│   │   ├── app.py                   # Main application
│   │   ├── config/
│   │   │   ├── settings.py          # Configuration
│   │   │   └── logger.py            # Logging setup
│   │   ├── database/
│   │   │   ├── __init__.py          # Database initialization
│   │   │   ├── models.py            # SQLAlchemy models
│   │   │   └── repository.py        # Database operations
│   │   ├── models/
│   │   │   └── cluster_models.py    # Data classes
│   │   ├── namespaces/
│   │   │   ├── cluster/             # Cluster API
│   │   │   ├── applications/        # Applications API
│   │   │   ├── jobs/                # Jobs API
│   │   │   └── nodes/               # Nodes API
│   │   └── services/
│   │       └── yarn_client.py       # YARN REST API client
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   └── README.md
│
├── rest-client/                     # React web client
│   ├── src/
│   │   ├── components/              # React components
│   │   ├── pages/                   # Page components
│   │   ├── services/                # API services
│   │   ├── types/                   # TypeScript types
│   │   ├── hooks/                   # Custom hooks
│   │   └── context/                 # App context
│   ├── package.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   └── README.md
│
├── docker-compose.yml               # Docker Compose configuration
└── README.md                        # This file
```

## Prerequisites

### For All Implementations
- Java 8+ (OpenJDK recommended)
- Python 3.9+
- Node.js 18+ (for web client)
- Access to a Hadoop YARN cluster

### For Hadoop MapReduce
- Apache Hadoop 3.x
- Maven 3.x

### For Apache Spark
- Apache Spark 3.x
- PySpark
- py4j

### For REST Server
- Python 3.11+
- Flask
- Flask-RESTX
- SQLAlchemy

### For Web Client
- React 19+
- TypeScript 6+
- Vite 8+
- Material-UI 9+

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd github-event-aggregation-ranking
```

### 2. Build Hadoop JAR

```bash
cd hadoop
mvn clean package -DskipTests
cd ..
```

### 3. Upload Resources to HDFS

```bash
# Create directories
hdfs dfs -mkdir -p /user/hadoop/jars
hdfs dfs -mkdir -p /user/hadoop/scripts

# Upload Hadoop JAR
hdfs dfs -put hadoop/target/hadoop-1.0-SNAPSHOT.jar /user/hadoop/jars/

# Upload Spark script
hdfs dfs -put spark/main.py /user/hadoop/scripts/spark/main.py

# Upload Python script
hdfs dfs -put python-non-parallel/main.py /user/hadoop/scripts/python/main.py

# Verify
hdfs dfs -ls /user/hadoop/jars/
hdfs dfs -ls /user/hadoop/scripts/
```

### 4. Start the REST Server

```bash
cd rest-server
cp .env.example .env
# Edit .env with your configuration

pip install -r requirements.txt
python src/app.py
```

### 5. Start the Web Client

```bash
cd rest-client
npm install
npm run dev
```

### 6. Access the Application

- **Web Client**: http://localhost:3000
- **API Documentation**: http://localhost:5000/docs
- **API Base URL**: http://localhost:5000/api

## REST API Server

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/cluster/info` | Cluster information |
| GET | `/api/cluster/metrics` | Cluster metrics |
| GET | `/api/cluster/scheduler` | Scheduler information |
| GET | `/api/applications/` | List applications |
| GET | `/api/applications/{id}` | Application details |
| PUT | `/api/applications/{id}/state` | Kill application |
| POST | `/api/applications/submit` | Submit application |
| GET | `/api/jobs/` | List jobs |
| GET | `/api/jobs/types` | Available job types |
| POST | `/api/jobs/submit` | Submit job |
| GET | `/api/jobs/{id}` | Job status |
| GET | `/api/jobs/{id}/result` | Job results |
| PUT | `/api/jobs/{id}/kill` | Kill job |
| GET | `/api/jobs/{id}/logs` | Job logs |
| GET | `/api/nodes/` | List nodes |
| GET | `/api/nodes/{id}` | Node details |
| GET | `/api/nodes/statistics` | Node statistics |
| GET | `/api/nodes/health` | Node health |

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `5000` |
| `DEBUG` | Debug mode | `false` |
| `YARN_RM_HOST` | YARN ResourceManager host | `10.1.1.144` |
| `YARN_RM_PORT` | YARN ResourceManager port | `8088` |
| `DATABASE_URL` | SQLite database URL | `sqlite:///data/jobs.db` |
| `HADOOP_HOME` | Hadoop installation path | `/opt/hadoop` |
| `SPARK_HOME` | Spark installation path | `/opt/spark` |
| `HADOOP_JAR_PATH` | Hadoop JAR path on HDFS | `hdfs://...` |
| `SPARK_SCRIPT` | Spark script path on HDFS | `hdfs://...` |
| `PYTHON_NON_PARALLEL_SCRIPT` | Python script path on HDFS | `hdfs://...` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Web Client

### Pages

| Route | Page | Description |
|-------|------|-------------|
| `/` | Dashboard | Cluster overview, metrics, charts |
| `/applications` | Applications | List and manage YARN applications |
| `/applications/:id` | Application Detail | Detailed application view |
| `/jobs` | Jobs | List submitted jobs |
| `/jobs/submit` | Submit Job | Multi-step job submission wizard |
| `/jobs/:id` | Job Detail | Job status, logs, results |
| `/nodes` | Nodes | Cluster nodes monitoring |

### Job Types

The web client supports submitting three types of jobs:

1. **Hadoop MapReduce** - Distributed batch processing
2. **Apache Spark** - In-memory distributed processing
3. **Python Non-Parallel** - Sequential processing

## Implementations Comparison

| Feature | Hadoop MapReduce | Apache Spark | Python Non-Parallel |
|---------|-----------------|--------------|---------------------|
| Language | Java | Python | Python |
| Processing | Distributed (disk-based) | Distributed (in-memory) | Sequential |
| Jobs | 2 MapReduce jobs | 2 RDD operations | Single script |
| Memory Usage | Low (spills to disk) | Medium (in-memory) | High (all data in RAM) |
| Speed | Slow-Medium | Fast | Slow |
| Fault Tolerance | Yes | Yes | No |
| Best For | Very large datasets | Large datasets | Small datasets |

## Docker Deployment

### Using Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Individual Services

```bash
# REST Server
docker build -t yarn-rest-server ./rest-server
docker run -d -p 5000:5000 yarn-rest-server

# Web Client
docker build -t yarn-rest-client ./rest-client
docker run -d -p 80:80 yarn-rest-client
```

## Development

### Building Hadoop JAR

```bash
cd hadoop
mvn clean package
```

### Running Spark Locally

```bash
cd spark
export SPARK_HOME=/opt/spark
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-*.zip
python main.py <input_dir> <output_dir> <N>
```

### Running Python Non-Parallel Locally

```bash
cd python-non-parallel
python main.py <input_dir> <output_dir> <N>
```

### REST Server Development

```bash
cd rest-server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/app.py
```

### Web Client Development

```bash
cd rest-client
npm install
npm run dev
```

## Troubleshooting

### Common Issues

**1. CORS Errors**
- Ensure Flask-CORS is configured
- Use Vite proxy for development

**2. YARN Connection Issues**
- Verify `YARN_RM_HOST` and `YARN_RM_PORT`
- Test: `curl http://<YARN_RM_HOST>:<YARN_RM_PORT>/ws/v1/cluster/info`

**3. JAR Not Found**
- Upload JAR to HDFS: `hdfs dfs -put hadoop-1.0-SNAPSHOT.jar /user/hadoop/jars/`
- Use full HDFS URI in paths

**4. AM Resource Limit Exceeded**
- Kill stuck applications: `yarn application -kill <app_id>`
- Reduce `max-app-attempts` to 1

**5. Java/Scala Classpath Issues**
- Set `JAVA_HOME` correctly: `/usr/lib/jvm/java-8-openjdk-amd64`
- Use absolute paths for executables

**6. Python Module Not Found**
- Set `PYTHONPATH` for PySpark: `$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-*.zip`

## License

This project is being developed as part of the Cloud Computing course within the "Artificial Intelligence and Data Engineering" program at the University of Pisa.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Contact

For questions or support, please contact the development team.

