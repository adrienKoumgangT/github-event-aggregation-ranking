# GitHub Events Aggregation - Apache Spark

PySpark implementation for aggregating and ranking GitHub Archive events.

## Overview

This Spark application processes GitHub Archive event data to:
1. **Event Count**: Count events per repository, date, and event type
2. **Top N Events**: Rank top N events per date across all repositories

## Architecture

```
Input (JSON files)
    │
    ▼
┌─────────────────────────┐
│ Map 1: extract_repo_event │  Parse JSON → (repo_id, date, event_type), 1
└─────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│ Reduce 1: reduceByKey   │  Sum counts per key
└─────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│ Output 1: event_count   │  CSV: repo_id, date, event_type, count
└─────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│ Map 2: parse_event_count│  Transform to (date, event_type), count
└─────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│ Reduce 2: groupByKey    │  Group by date, sort by count, take top N
└─────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│ Output 2: top_events    │  CSV: date, event_type, count, ...
└─────────────────────────┘
```

## Prerequisites

- Python 3.11+
- Apache Spark 3.x
- PySpark
- Java 8+ (OpenJDK recommended)
- Hadoop YARN cluster (for distributed execution)

## Installation

### Local Development

```bash
# Install PySpark
pip install pyspark

# Or use the Spark installation
export SPARK_HOME=/opt/spark
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-*.zip
```

### Dependencies

- `pyspark` - Spark Python API
- `py4j` - Bridge between Python and Java (included with Spark)
- `json` - JSON parsing (standard library)
- `sys` - Command-line arguments (standard library)

## Usage

### Command Line

```bash
# Local execution
python main.py <input_dir> <output_dir> <N>

# Submit to YARN cluster
spark-submit \
  main.py \
  hdfs://hadoop-namenode:9820/user/hadoop/github-events-dataset \
  hdfs://hadoop-namenode:9820/user/hadoop/output \
  10
```

### Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `input_dir` | Directory containing input JSON files | `hdfs://.../github-events-dataset` |
| `output_dir` | Directory for output files | `hdfs://.../output` |
| `N` | Number of top events to return | `10` |

### Output

The application creates two output directories:

```
output_dir/
├── event_count/          # Event counts per repo/date/type
│   └── part-00000       # CSV: repo_id, date, event_type, count
└── top_events/          # Top N events per date
    └── part-00000       # CSV: date, event_type, count, ...
```

## Data Flow

### Input Format

JSON files from GitHub Archive:
```json
{
  "repo": {"id": 12345, "name": "owner/repo"},
  "type": "WatchEvent",
  "created_at": "2015-01-01T12:00:00Z"
}
```

### Intermediate Format (event_count)

```
12345, 2015-01-01, WatchEvent, 5
67890, 2015-01-01, PushEvent, 3
```

### Final Format (top_events)

```
2015-01-01, WatchEvent, 150, PushEvent, 120, IssuesEvent, 90
2015-01-02, PushEvent, 200, WatchEvent, 180, ForkEvent, 75
```

## Functions

### `extract_repo_event(line)`

Parses a JSON line and extracts event information.

- **Input**: JSON string
- **Output**: List containing tuple `((repo_id, date, event_type), 1)`
- **Error Handling**: Returns empty list for malformed lines

### `parse_event_count_output(line)`

Transforms event count output for top-N computation.

- **Input**: Tuple `("repo_id, date, event_type", count)`
- **Output**: Tuple `((date, event_type), count)`

## Configuration

Spark configuration can be set via `SparkConf`:

```python
conf = SparkConf() \
    .setAppName("github_events_aggregator_ranking")
```

## Running on YARN

### Via spark-submit

```bash
spark-submit \
  main.py \
  <input_dir> <output_dir> <N>
```

### Via REST API (Docker deployment)

The job can be submitted through the YARN REST API. 
The script is uploaded to HDFS and executed via `java` with Spark JARs in the classpath.

```bash
# Upload script to HDFS
hdfs dfs -mkdir -p /user/hadoop/scripts
hdfs dfs -put main.py /user/hadoop/scripts/spark_main.py
```

## Example

```bash
# Process GitHub events for top 3 per day
python main.py \
  hdfs://hadoop-namenode:9820/user/hadoop/github-events-dataset \
  hdfs://hadoop-namenode:9820/user/hadoop/output \
  3
```

Output:
```
event_count/part-00000:
12345, 2015-01-01, WatchEvent, 5
67890, 2015-01-01, PushEvent, 3
...

top_events/part-00000:
2015-01-01, WatchEvent, 150, PushEvent, 120, IssuesEvent, 90
2015-01-02, PushEvent, 200, WatchEvent, 180, ForkEvent, 75
...
```


## License

Part of the GitHub Event Aggregation Ranking project.
