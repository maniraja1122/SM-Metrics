from datetime import datetime

# Parse string as `datetime`` format. Currently supports two formats.
def parse_date(date_str):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S.%fZ"):  # Include more formats as needed
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"time data '{date_str}' does not match any expected format")