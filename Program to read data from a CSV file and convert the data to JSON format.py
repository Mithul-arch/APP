import csv
import json
import sys
from pathlib import Path


def csv_to_json(csv_file_path, json_file_path):
    """Read a CSV file and write its contents as JSON to json_file_path."""
    data = []

    with open(csv_file_path, mode="r", encoding="utf-8-sig", newline="") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)

    with open(json_file_path, mode="w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Converted {len(data)} rows from '{csv_file_path}' to '{json_file_path}'")


def main():
    if len(sys.argv) < 2:
        print("Usage: python csv_to_json.py <input.csv> [output.json]")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    json_file_path = sys.argv[2] if len(sys.argv) >= 3 else str(Path(csv_file_path).with_suffix(".json"))

    if not Path(csv_file_path).is_file():
        print(f"Error: '{csv_file_path}' does not exist.")
        sys.exit(1)

    csv_to_json(csv_file_path, json_file_path)


if __name__ == "__main__":
    main()