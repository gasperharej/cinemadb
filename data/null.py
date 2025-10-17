#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    print(f"Use: {sys.argv[0]} <input_file.csv>")
    sys.exit(1)

input_file = Path(sys.argv[1])
if not input_file.exists():
    print(f"Error: file {input_file} does not exist.")
    sys.exit(1)

output_file = input_file.with_name(input_file.stem + ".null.csv")

with open(input_file, "r", encoding="utf-8") as infile, \
     open(output_file, "w", encoding="utf-8") as outfile:

    for line in infile:
        new_line = line.replace('"\\N"', r'\N')
        outfile.write(new_line)

print(f"File has been processed and saved as {output_file}")
