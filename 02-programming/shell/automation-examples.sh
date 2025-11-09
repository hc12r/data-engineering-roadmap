#!/usr/bin/env bash
# Simple automation examples

echo "Start"
DATE=$(date '+%Y-%m-%d')
echo "Today is $DATE"
# Example: iterate files
for f in *.csv; do
  [ -e "$f" ] || continue
  echo "Processing $f"
done
