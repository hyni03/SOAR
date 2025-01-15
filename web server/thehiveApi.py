import requests
import json
import hashlib

API_URL = "http://localhost:9000/thehive/api/v1"
AUTH_TOKEN = "Bearer mVzBsze4PnyupMos9406IE66BuZ7sHlH"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": AUTH_TOKEN
}

def create_case(title, description, case_template='Phishing Analysis Template'):
    payload = {
        "title": title,
        "description": description,
        "endDate": 1640000000000,
        "tags": ["email-rep"],
        "flag": False,
        "status": "New",
        "caseTemplate": case_template
    }

    try:
        response = requests.post(f"{API_URL}/case", headers=HEADERS, data=json.dumps(payload))
        if response.status_code in [200, 201]:
            return response.json().get('_id')
        else:
            print(f"Case 생성 실패: {response.status_code}, {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Case 생성 중 오류 발생: {e}")
        return None


def create_observable(case_id, hash_val):
    payload = {
        "dataType": "hash",
        "data": hash_val,
        "tags": ["phishing"],
        "ioc": True,
        "isZip": False
    }

    try:
        response = requests.post(f"{API_URL}/case/{case_id}/observable", headers=HEADERS, data=json.dumps(payload))
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return f"Observable 생성 실패: {response.status_code}, {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Observable 생성 중 오류 발생: {e}"


def calculate_hash(file_path):
    try:
        with open(file_path, "rb") as file:
            file_data = file.read()
            return hashlib.md5(file_data).hexdigest()
    except Exception as e:
        print(f"해시 계산 중 오류 발생: {e}")
        return None
