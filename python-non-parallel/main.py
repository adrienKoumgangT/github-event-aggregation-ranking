import json
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Optional, Dict


def read_files_recursive(directory: str):
    for path in Path(directory).rglob("*"):
        if path.is_file():
            try:
                content = path.read_text(encoding="utf-8")
                yield path, content
            except Exception as e:
                print(f"Error reading {path}: {e}")


def extra_event_count_line_key(line: str) -> Optional[str]:
    event_dict = json.loads(line)
    try:
        return f"{event_dict['repo']['id']}, {event_dict['created_at'].split('T')[0]}, {event_dict['type']}"
    except Exception as e:
        print(f"Error reading {line}: {e}")
    return None


def convert_ns_to_hours_format(time_in_ns: int) -> str:
    # Convert nanoseconds to milliseconds
    time_in_ms = time_in_ns / 1_000_000

    # Calculate hours, minutes, seconds, and milliseconds
    hours = int(time_in_ms / (1000 * 60 * 60))
    minutes = int((time_in_ms % (1000 * 60 * 60)) / (1000 * 60))
    seconds = int((time_in_ms % (1000 * 60)) / 1000)
    milliseconds = int(time_in_ms % 1000)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


if __name__ == '__main__':

    # check the input
    if len(sys.argv) < 4:
        print("Usage: main.py <input dir> <output dir> N", file=sys.stderr)
        sys.exit(-1)

    tracemalloc.start()

    program_start = time.time_ns()

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    N = int(sys.argv[3])

    print(f"input dir: {input_dir}")
    print(f"output dir: {output_dir}")
    print(f"N: {N}")

    event_count_output_file = Path(output_dir) / "event_count.txt"
    top_events_output_file = Path(output_dir) / "top_events.txt"

    # key: repo.id, create_at, type --- value: count
    event_count_dict: Dict[str, int] = dict()

    event_count_start = time.time_ns()
    for path, content in read_files_recursive(input_dir):
        print(f"=== {path} ===")
        # print(f"first line: {content.split('\n')[0]}")

        for line in content.split('\n'):
            if line:
                key = extra_event_count_line_key(line)
                if key:
                    if key in event_count_dict:
                        event_count_dict[key] += 1
                    else:
                        event_count_dict[key] = 1
    event_count_duration = time.time_ns() - event_count_start

    with open(event_count_output_file, "w") as event_count_file:
        event_count_file.write(
            "\n".join(
                f"{key}, {value}"
                for key, value in event_count_dict.items()
            )
        )

    # key: create --- value: eventType, count
    top_events_dict: Dict[str, Dict[str, int]] = dict()

    top_events_start = time.time_ns()
    for k, v in event_count_dict.items():
        keys = k.split(",")
        if len(keys) == 3:
            if keys[1] and keys[2]:
                create_at = keys[1].strip()
                event_type = keys[2].strip()

                if create_at in top_events_dict:
                    event = top_events_dict[create_at]
                    if event_type in event:
                        event[event_type] += v
                    else:
                        event[event_type] = v
                else:
                    top_events_dict[create_at] = {event_type: v}
    top_events_duration = time.time_ns() - top_events_start

    with open(top_events_output_file, "w") as top_events_file:
        top_events_file.write(
            "\n".join(
                f"{key}, {', '.join(f'{k}, {v}' for k, v in (value.items() if len(value.keys()) <= N else sorted(value.items(), key=lambda x: x[1], reverse=True)[:N]))}"
                for key, value in top_events_dict.items()
            )
        )

    program_duration = time.time_ns() - program_start

    print()
    print(f"program duration: {convert_ns_to_hours_format(program_duration)}")
    print(f"- event count duration: {convert_ns_to_hours_format(event_count_duration)}")
    print(f"- top events duration: {convert_ns_to_hours_format(top_events_duration)}")

    current, peak = tracemalloc.get_traced_memory()

    print()
    print(f"Current memory: {current / 1024 / 1024:.2f} MB")
    print(f"Peak memory: {peak / 1024 / 1024:.2f} MB")

    tracemalloc.stop()

