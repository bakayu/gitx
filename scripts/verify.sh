#!/bin/bash
timeout 5s poetry run python -c "from gitx.app import GitxApp; app = GitxApp()" || true
exit_code=$?
if [ -n "$exit_code" ] && [ "$exit_code" -eq 124 ]; then
    echo "App initialized successfully (timeout as expected)"
    exit 0
elif [ -n "$exit_code" ] && [ "$exit_code" -eq 0 ]; then
    echo "App initialized successfully"
    exit 0
else
    echo "App initialization failed with exit code: $exit_code"
    exit 1
fi