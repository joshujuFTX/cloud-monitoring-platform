from fastapi import FastAPI, Query
import psutil

from app.db import Base, engine
from app.healthchecks.alerts import get_alerts
from app.healthchecks.checks import check_url
from app.healthchecks.services import check_all_services
from app.persistence import get_history, save_alerts, save_metrics, save_service_checks

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cloud Monitoring Platform",
    description="Infrastructure monitoring API for system health, service checks, alerts, and historical metrics.",
    version="1.1.0",
)


@app.get("/")
def root():
    return {
        "service": "Cloud Monitoring Platform",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.get("/metrics")
def metrics():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    data = {
        "cpu_percent": psutil.cpu_percent(interval=0.5),
        "memory_percent": memory.percent,
        "memory_used_gb": round(memory.used / (1024**3), 2),
        "memory_total_gb": round(memory.total / (1024**3), 2),
        "disk_percent": disk.percent,
        "disk_used_gb": round(disk.used / (1024**3), 2),
        "disk_total_gb": round(disk.total / (1024**3), 2),
    }

    save_metrics(data)
    return data


@app.get("/system")
def system_info():
    import platform
    import socket
    import sys

    return {
        "hostname": socket.gethostname(),
        "operating_system": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": sys.version.split()[0],
    }


@app.get("/alerts")
def alerts():
    results = get_alerts()
    save_alerts(results)
    return results


@app.get("/services")
def services():
    results = check_all_services()
    save_service_checks(results)
    return results


@app.get("/check")
def service_check(url: str):
    return check_url(url)


@app.get("/history")
def history(
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Number of recent records to return from each category.",
    )
):
    return get_history(limit)
