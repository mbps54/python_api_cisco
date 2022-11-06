import requests
import json
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def fdm_login(
    fdm_ip: str,
    fdm_port: int,
    api_version: int,
    tmp_dir: str,
    username: str,
    password: str,
    ) -> str:
    print("Getting auth token:")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer",
    }
    payload = {"grant_type": "password", "username": username, "password": password}
    request = requests.post(
        f"https://{fdm_ip}:{fdm_port}/api/fdm/v{api_version}/fdm/token",
        json=payload,
        verify=False,
        headers=headers,
    )
    if request.status_code == 400:
        raise Exception(f"Error logging in: {request.content}")
    try:
        access_token = request.json()["access_token"]
        fa = open("{}/token".format(tmp_dir), "w")
        fa.write(access_token)
        fa.close()
        print("  - Token saved to file")
        return access_token
    except:
        raise Exception("Can not write file token")
