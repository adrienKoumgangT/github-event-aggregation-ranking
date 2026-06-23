import json
import sys
from pyspark import SparkConf, SparkContext


def extract_repo_event(line):
    """
    Safely parses a JSON line. Returns a list containing a single key-value tuple
    """
    if not line.strip():
        return []
    try:
        event_dict = json.loads(line)
        key = f"{event_dict.get('repo').get('id')}, {event_dict.get('created_at').split('T')[0]}, {event_dict.get('type')}"
        return [(key, 1)]
    except Exception:
        # Silently ignore malformed lines/missing keys
        return []


def parse_event_count_output(line):
    """
    Parses a tuple like ('12345, 2011-09-06, WatchEvent', 5) and returns a tuple: (('2011-09-06', 'WatchEvent'), 5)
    """
    # Separate the key string from the count integer
    key_string = line[0]
    count = line[1]

    parts = [part.strip() for part in key_string.split(',')]

    # parts[0] is the repo.id
    date = parts[1]
    event_type = parts[2]

    return (date, event_type), count


if __name__ == "__main__":

    # check the input
    if len(sys.argv) < 4:
        print("Usage: main.py <input dir> <output dir> N", file=sys.stderr)
        sys.exit(-1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    if output_dir[-1] != '/':
        output_dir += '/'
    N = int(sys.argv[3])

    # define the SparkContext
    conf = SparkConf().setAppName("github_events_aggregator_ranking")
    sc = SparkContext(conf=conf)

    # apply MapReduce
    lines = sc.textFile(input_dir)

    # --- event count

    repo_events = lines.flatMap(extract_repo_event)

    counts = repo_events.reduceByKey(lambda x, y: x + y)

    (counts.map(lambda x: f"{x[0]}, {x[1]}")
     .repartition(1).saveAsTextFile(output_dir + "event_count"))

    # --- top events

    date_event_keys = counts.map(lambda repo_event: parse_event_count_output(repo_event))
    date_event_keys_total = date_event_keys.reduceByKey(lambda x, y: x + y)

    date_events_grouped = date_event_keys_total.map(lambda x: (x[0][0], (x[0][1], x[1]))).groupByKey()

    top_n_events = date_events_grouped.mapValues(
        lambda events: sorted(list(events), key=lambda item: item[1], reverse=True)[:N]
    )

    formatted_top_events = top_n_events.map(
        lambda x: f"{x[0]}, " + ", ".join([f"{k}, {v}" for k, v in x[1]])
    )

    formatted_top_events.repartition(1).saveAsTextFile(output_dir + "top_events")

