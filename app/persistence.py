from sqlalchemy import select

from app.db import SessionLocal
from app.models import AlertEvent, MonitoringMetric, ServiceCheck


def save_metrics(data: dict):
    db = SessionLocal()
    try:
        record = MonitoringMetric(
            cpu_percent=data["cpu_percent"],
            memory_percent=data["memory_percent"],
            disk_percent=data["disk_percent"],
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    finally:
        db.close()


def save_service_checks(results: list[dict]):
    db = SessionLocal()
    try:
        records = []

        for result in results:
            record = ServiceCheck(
                url=result["url"],
                status=result["status"],
                status_code=result.get("status_code"),
                response_time_ms=result["response_time_ms"],
                error=result.get("error"),
            )
            db.add(record)
            records.append(record)

        db.commit()
        return records
    finally:
        db.close()


def save_alerts(alerts: list[dict]):
    if not alerts:
        return

    db = SessionLocal()
    try:
        for alert in alerts:
            db.add(
                AlertEvent(
                    type=alert["type"],
                    severity=alert["severity"],
                    url=alert["url"],
                    message=alert["message"],
                )
            )

        db.commit()
    finally:
        db.close()


def get_history(limit: int = 20):
    db = SessionLocal()

    try:
        metrics = db.scalars(
            select(MonitoringMetric)
            .order_by(MonitoringMetric.timestamp.desc())
            .limit(limit)
        ).all()

        services = db.scalars(
            select(ServiceCheck)
            .order_by(ServiceCheck.timestamp.desc())
            .limit(limit)
        ).all()

        alerts = db.scalars(
            select(AlertEvent)
            .order_by(AlertEvent.timestamp.desc())
            .limit(limit)
        ).all()

        return {
            "metrics": [
                {
                    "id": item.id,
                    "timestamp": item.timestamp,
                    "cpu_percent": item.cpu_percent,
                    "memory_percent": item.memory_percent,
                    "disk_percent": item.disk_percent,
                }
                for item in metrics
            ],
            "service_checks": [
                {
                    "id": item.id,
                    "timestamp": item.timestamp,
                    "url": item.url,
                    "status": item.status,
                    "status_code": item.status_code,
                    "response_time_ms": item.response_time_ms,
                    "error": item.error,
                }
                for item in services
            ],
            "alerts": [
                {
                    "id": item.id,
                    "timestamp": item.timestamp,
                    "type": item.type,
                    "severity": item.severity,
                    "url": item.url,
                    "message": item.message,
                }
                for item in alerts
            ],
        }
    finally:
        db.close()
