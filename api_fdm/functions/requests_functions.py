import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from functions.basic_functions import debugger


def request_get(
    fdm_ip: str,
    fdm_port: int,
    api_version: int,
    api_path: str,
    tmp_dir: str,
    token: str,
    ) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(token),
    }
    api_url = f"https://{fdm_ip}:{fdm_port}/api/fdm/v{api_version}/{api_path}"
    debugger(api_url, "GET request with no payload", tmp_dir)
    request = requests.get(api_url, headers=headers, verify=False)
    debugger(api_url, request.text, tmp_dir)
    return request


def request_post(
    fdm_ip: str,
    fdm_port: int,
    api_version: int,
    api_path: str,
    tmp_dir: str,
    token: str,
    payload: dict,
    ) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(token),
    }
    api_url = f"https://{fdm_ip}:{fdm_port}/api/fdm/v{api_version}/{api_path}"
    debugger(api_url, payload, tmp_dir)
    request = requests.post(api_url, json=payload, headers=headers, verify=False)
    debugger(api_url, request.text, tmp_dir)
    return request


def request_post_np(
    fdm_ip: str,
    fdm_port: int,
    api_version: int,
    api_path: str,
    tmp_dir: str,
    token: str,
    ) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(token),
    }
    api_url = f"https://{fdm_ip}:{fdm_port}/api/fdm/v{api_version}/{api_path}"
    debugger(api_url, "POST request with no payload", tmp_dir)
    request = requests.post(api_url, headers=headers, verify=False)
    debugger(api_url, request.text, tmp_dir)
    return request

