import json
import sys
from pyspark import SparkConf, SparkContext


if __name__ == "__main__":

    # check the input
    if len(sys.argv) < 3:
        print("Usage: wordcount_file.py <input dir> <output dir>", file=sys.stderr)
        sys.exit(-1)

    # define the SparkContext
    conf = SparkConf().setAppName("wordcount_file")
    sc = SparkContext(conf=conf)

    # apply MapReduce
    lines = sc.textFile(sys.argv[1])
    event_dicts = lines.flatMap(lambda x: json.loads(x))
    repo_events = event_dicts.map(lambda x: (f"{x['repo']['id']}, {x['create_at']}, {x['type']}", 1))
    counts = repo_events.reduceByKey(lambda x, y: x + y)

    # repartition(1) returns an RDD consisting of 1 partition
    counts.repartition(1).saveAsTextFile(sys.argv[2])

    # example of result:
    # ('repo.id, create_at, type', count)
    # ('12345, 2011-09-06T17:26:27Z, WatchEvent', 5)

