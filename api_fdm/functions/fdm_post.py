import json
from typing import Union
from functions.requests_functions import request_post
from functions.fdm_login import fdm_login


def fdm_post(
    fdm_ip: str,
    fdm_port: int,
    api_version: int,
    api_path: str,
    payload: str,
    tmp_dir: str,
    username: str,
    password: str,
    ) -> Union[dict, str]:
    token_file = open("{}/token".format(tmp_dir), "r")
    token = token_file.readline()
    token_file.close()
    print(f'{api_path}:')
    try:
        request = request_post(
            fdm_ip, fdm_port, api_version, api_path, tmp_dir, token, payload
        )
        if request.status_code == 401:
            print("Error 401, auth token is not valid")
            token = fdm_login(
                fdm_ip, fdm_port, api_version, tmp_dir, username, password
            )
            request = request_post(
                fdm_ip, fdm_port, api_version, api_path, tmp_dir, payload, token
            )
        if request.status_code == 422:
            print("  - POST error (422)")
            return request.status_code
        if request.status_code == 200:
            print("  - POST success (200)")
        else:
            print("  - POST error")
            return request.status_code
        return request.json()
    except:
        raise Exception("Something went wrong, see debug.log file")
