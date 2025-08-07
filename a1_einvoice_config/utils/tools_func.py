"""
    contains func check , convert ..
"""
from odoo.http import request
from datetime import datetime
import requests
from ..utils.const_params import api_url


def document_hash_sha256(base64_str):
    # Decode Base64
    decode_base64 = base64.b64decode(base64_str)
    # Encode the hash in base64
    sha256_hash = sha256(decode_base64).hexdigest()
    return sha256_hash


def base64_encode_json(json_str):
    json_bytes = json_str.encode("utf-8")
    return base64.b64encode(json_bytes)


def handle_response(code, message, details):
    return {
        "code": code,
        "message": message,
        "data": {"details": details}
    }


def handle_authenticate(access_token):
    if not access_token:
        return handle_response(code=401, message="Unauthorized", details="Access Token is missing")
    if access_token:
        is_valid_token = request.env['einvoice.authenticate'].sudo().search([
            ('access_token', '=', access_token),
            ('token_expire', '>', datetime.utcnow())], limit=1)
        if not is_valid_token:
            return handle_response(code=401, message="Unauthorized", details="Access Token is wrong or expired")


def action_validate_tin(vat, identification_type, identification_number, access_token):
    url = f"https://{api_url}/api/v1.0/taxpayer/validate/{vat}?idType={identification_type}&idValue={identification_number}"

    payload = {}
    headers = {"Authorization": "Bearer %s" % access_token}
    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        return 'valid'
    else:
        return 'invalid'

