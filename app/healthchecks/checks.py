import time

import requests


def check_url(url: str, timeout: int = 5):
    start = time.perf_counter()

    try:
        response = requests.get(url, timeout=timeout)
        response_time_ms = round((time.perf_counter() - start) * 1000, 2)

        return {
            "url": url,
            "status": "healthy" if response.ok else "unhealthy",
            "status_code": response.status_code,
            "response_time_ms": response_time_ms,
        }

    except requests.RequestException as error:
        response_time_ms = round((time.perf_counter() - start) * 1000, 2)

        return {
            "url": url,
            "status": "unhealthy",
            "status_code": None,
            "response_time_ms": response_time_ms,
            "error": str(error),
        }
