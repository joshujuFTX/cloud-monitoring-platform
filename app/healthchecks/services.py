from app.healthchecks.checks import check_url

SERVICES = [
    "https://example.com",
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/503",
]

def check_all_services():
    return [check_url(url) for url in SERVICES]
