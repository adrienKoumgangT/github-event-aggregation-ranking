# GitHub Events Aggregation - Python Non-Parallel

Single-threaded Python implementation for aggregating and ranking GitHub Archive events.
This implementation processes data sequentially without parallelization for comparison with distributed approaches.

## Overview

This Python application processes GitHub Archive event data to:
1. **Event Count**: Count events per repository, date, and event type
2. **Top N Events**: Rank top N events per date across all repositories
3. **Performance Metrics**: Track execution time and memory usage

## Architecture

```
Input (JSON files)
    │
    ▼
┌──────────────────────────┐
│ read_files_recursive()   │  Iterate through all files in directory
└──────────────────────────┘
    │
    ▼
┌──────────────────────────┐
│ extra_event_count_line_key() │  Parse JSON → repo_id, date, event_type
└──────────────────────────┘
    │
    ▼
┌──────────────────────────┐
│ event_count_dict        │  Dictionary: key → count (in-memory)
└──────────────────────────┘
    │
    ├──────────────────────────┐
    ▼                          ▼
┌──────────────────┐  ┌──────────────────┐
│ event_count.txt  │  │ top_events_dict  │  Group by date, sort, take top N
└──────────────────┘  └──────────────────┘
                           │
                           ▼
                      ┌──────────────────┐
                      │ top_events.txt   │
                      └──────────────────┘
```

## Prerequisites

- Python 3.11+
- Standard library only (no external dependencies)

## Installation

No external dependencies required. Uses only standard library modules:

```bash
# Standard library modules used:
- json (JSON parsing)
- sys (command-line arguments)
- time (performance timing)
- tracemalloc (memory tracking)
- pathlib (file system operations)
```

## Usage

### Command Line

```bash
python main.py <input_dir> <output_dir> <N>
```

### Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `input_dir` | Directory containing input JSON files | `/data/github-events` |
| `output_dir` | Directory for output files | `/data/output` |
| `N` | Number of top events to return | `10` |

### Output

The application creates two output files:

```
output_dir/
├── event_count.txt      # Event counts per repo/date/type
└── top_events.txt       # Top N events per date
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

### Output Format

**event_count.txt:**
```
12345, 2015-01-01, WatchEvent, 5
67890, 2015-01-01, PushEvent, 3
```

**top_events.txt:**
```
2015-01-01, WatchEvent, 150, PushEvent, 120, IssuesEvent, 90
2015-01-02, PushEvent, 200, WatchEvent, 180, ForkEvent, 75
```

## Functions

### `read_files_recursive(directory)`

Generator that recursively reads all files in a directory.

- **Input**: Directory path
- **Output**: Yields `(path, content)` tuples
- **Error Handling**: Prints and skips files that can't be read

### `extra_event_count_line_key(line)`

Parses a JSON line and extracts event information.

- **Input**: JSON string
- **Output**: Key string `"repo_id, date, event_type"` or `None`
- **Error Handling**: Returns `None` for malformed lines

### `convert_ns_to_hours_format(time_in_ns)`

Converts nanoseconds to human-readable format.

- **Input**: Time in nanoseconds
- **Output**: String in `HH:MM:SS.mmm` format

## Performance

The application tracks:

- **Program duration**: Total execution time
- **Event count duration**: Time for first aggregation pass
- **Top events duration**: Time for second aggregation pass
- **Current memory**: Memory in use after processing
- **Peak memory**: Maximum memory used during processing

Example output:
```
program duration: 00:00:05.234
- event count duration: 00:00:03.456
- top events duration: 00:00:01.778

Current memory: 45.23 MB
Peak memory: 128.56 MB
```

## Example

```bash
python main.py \
  /data/github-events-dataset \
  /data/output \
  10
```

Console output:
```
input dir: /data/github-events-dataset
output dir: /data/output
N: 10
=== /data/github-events-dataset/2015-01-01.json ===
=== /data/github-events-dataset/2015-01-02.json ===

program duration: 00:00:05.234
- event count duration: 00:00:03.456
- top events duration: 00:00:01.778

Current memory: 45.23 MB
Peak memory: 128.56 MB
```


## HDFS Integration

When running on Hadoop cluster nodes, use `hdfs dfs` commands to copy data:

```bash
# Copy input from HDFS
hdfs dfs -get hdfs://hadoop-namenode:9820/user/hadoop/input/* /tmp/input/

# Run script
python main.py /tmp/input /tmp/output 10

# Copy output to HDFS
hdfs dfs -put /tmp/output/* hdfs://hadoop-namenode:9820/user/hadoop/output/
```

## License

Part of the GitHub Event Aggregation Ranking project.
