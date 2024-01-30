from fastapi import Request
import re


def check_headers(headers: Request.headers) -> list:
    expected_headers = ["User-Agent", "Accept-Language"]
    not_found = [
        header for header in expected_headers if header not in headers
    ]

    return not_found


def validate_headers(headers: Request.headers):
    pattern = r"(?i:(?:\*|[a-z\-]{2,5})(?:;q=\d\.\d)?,)+(?:\*|[a-z\-]{2,5})(?:;q=\d\.\d)?"

    return re.match(pattern, headers["Accept-Language"])
