from fastapi import FastAPI
import psutil
from app.healthchecks.checks import check_url
from app.healthchecks.services import check_all_services
from app.healthchecks.alerts import get_alerts

app = FastAPI(
    title="Cloud Monitoring Platform",
    description="Infrastructure monitoring API for system health and resource metrics.",
    version="1.0.0",
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

    return {
        "cpu_percent": psutil.cpu_percent(interval=0.5),
        "memory_percent": memory.percent,
        "memory_used_gb": round(memory.used / (1024**3), 2),
        "memory_total_gb": round(memory.total / (1024**3), 2),
        "disk_percent": disk.percent,
        "disk_used_gb": round(disk.used / (1024**3), 2),
        "disk_total_gb": round(disk.total / (1024**3), 2),
    }


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
    return get_alerts()


@app.get("/services")
def services():
    return check_all_services()


@app.get("/check")
def service_check(url: str):
    return check_url(url)
