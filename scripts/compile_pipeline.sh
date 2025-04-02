#!/bin/bash

# Set the directory you want to change to
TARGET_DIR="../"

# Change to the directory
cd "$TARGET_DIR" || { echo "Failed to change directory"; exit 1; }

# Run the Python script
python -m pipeline.pipeline


