import ast
import sys
from pyspark import SparkConf, SparkContext


def parse_event_count_output(line):
    """
    Parses a string like "('12345, 2011-09-06T17:26:27Z, WatchEvent', 5)"
    and returns a tuple: ('2011-09-06T17:26:27Z', ('WatchEvent', 5))
    """
    # Safely convert the raw string back into a Python tuple
    # Result: ('12345, 2011-09-06T17:26:27Z, WatchEvent', 5)
    parsed_tuple = ast.literal_eval(line)

    # Separate the key string from the count integer
    key_string = parsed_tuple[0]
    count = parsed_tuple[1]

    # Split the comma-separated key string and remove extra whitespace
    parts = [part.strip() for part in key_string.split(',')]

    # Extract the elements (parts[0] is the repo.id, which we are discarding here)
    date = parts[1]
    event_type = parts[2]

    return date, (event_type, count)



if __name__ == "__main__":

    # check the input
    if len(sys.argv) < 3:
        print("Usage: top_events.py <input file> <output dir>", file=sys.stderr)
        sys.exit(-1)

    # define the SparkContext
    conf = SparkConf().setAppName("top_events")
    sc = SparkContext(conf=conf)

    lines = sc.textFile(sys.argv[1])
    event_types = lines.map(lambda line: parse_event_count_output(line))
    # key: create_at; value: event_type, count
    # TODO: define reduce
    counts = event_types.reduceByKey(lambda x, y: x + y)




    # repartition(1) returns an RDD consisting of 1 partition
    counts.repartition(1).saveAsTextFile(sys.argv[2])
