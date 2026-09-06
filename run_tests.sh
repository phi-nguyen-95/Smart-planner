#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

export SMART_PLANNER_DATABASE_URL="sqlite:///$PROJECT_ROOT/test_weather.db"

echo "Using isolated test database:"
echo "$SMART_PLANNER_DATABASE_URL"
echo

# Always remove the test database when finished.
cleanup() {
    rm -f "$PROJECT_ROOT/test_weather.db"
}

trap cleanup EXIT

python3 -m unittest discover \
    -s tests \
    -p "test_*.py" \
    -v
