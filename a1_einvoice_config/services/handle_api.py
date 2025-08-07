"""
    handle api
"""
import requests


def get_access_token(api_url, client_id, client_secret, grant_type, scope):
    url = f"https://{api_url}/connect/token"
    payload = f"client_id={client_id.strip()}&client_secret={client_secret.strip()}&grant_type=" \
              f"{grant_type.strip()}&scope={scope.strip()}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.request("POST", url, headers=headers, data=payload)

    try:
        if response.status_code == 200:
            result = response.json()
            return result["access_token"]

    except Exception:
        return None




