#!/bin/bash

# Create necessary directories
mkdir -p logs
mkdir -p chrome_profiles

# Start Gunicorn
gunicorn -c gunicorn_config.py src.web.app:app