import requests
import json


def _ip_is_abusive(ip_addr, api_key, threshold=90):
    """Check if the given IP has an abuse confidence score greater than the given threshold percentage."""

    # The AbuseIPDB API endpoint
    url = "https://api.abuseipdb.com/api/v2/check"

    querystring = {"ipAddress": ip_addr, "maxAgeInDays": "90"}

    headers = {
        "Accept": "application/json",
        "Key": api_key,
    }

    response = requests.request(
        method="GET", url=url, headers=headers, params=querystring
    )
    data = json.loads(response.text)
    return data["data"]["abuseConfidenceScore"] > threshold
