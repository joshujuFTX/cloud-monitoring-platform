# Cloud Monitoring Platform

A Python-based infrastructure monitoring service that collects system metrics and exposes them through a REST API.

## Features

- CPU utilization monitoring
- Memory utilization monitoring
- Disk utilization monitoring
- System health endpoint
- Hostname and operating system information
- REST API built with FastAPI
- Linux system metrics collected with psutil

## Tech Stack

- Python
- FastAPI
- Uvicorn
- psutil
- Linux
- REST APIs

## API Endpoints

- GET / — service status
- GET /health — service health
- GET /metrics — CPU, memory, and disk metrics
- GET /system — system and host information
- GET /docs — interactive API documentation

## Running Locally

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
