import os
import requests
import base64
import json


def get_public_key() -> dict:
    keycloak_internal_url = os.getenv("API_APP_KEYCLOAK_INTERNAL_URL")
    realm = os.getenv("API_APP_KEYCLOAK_REALM")
    url = f"{keycloak_internal_url}/realms/{realm}/protocol/openid-connect/certs"

    resp = requests.get(url)
    resp.raise_for_status()

    jwks = resp.json()
    return jwks['keys'][0]


def check_role(token: str, role: str):
    parts = token.split('.')
    payload_b64 = parts[1]
    # Добавляем недостающие символы для Base64
    padding = '=' * ((4 - len(payload_b64) % 4) % 4)
    payload_b64 += padding

    # Декодируем Base64Url в байты
    decoded_bytes = base64.urlsafe_b64decode(payload_b64)

    # Преобразуем байты в строку JSON
    payload_json = decoded_bytes.decode('utf-8')

    # Парсим JSON в словарь
    payload = json.loads(payload_json)

    roles = payload.get('realm_access', {}).get('roles', [])

    if role not in roles:
        return False
    else:
        return True
