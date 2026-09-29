from app.healthchecks.services import check_all_services


def get_alerts():
    results = check_all_services()
    alerts = []

    for service in results:
        if service["status"] != "healthy":
            alerts.append({
                "type": "service_down",
                "severity": "critical",
                "url": service["url"],
                "message": f"Service is unhealthy: {service.get('error', service.get('status_code'))}",
            })

        elif service["response_time_ms"] > 1000:
            alerts.append({
                "type": "slow_response",
                "severity": "warning",
                "url": service["url"],
                "message": f"Response time is {service['response_time_ms']} ms",
            })

    return alerts
