import requests
import json
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from functions.fdm_login import fdm_login


def initial_auth(
    fdm_ip: str,
    fdm_port: int,
    api_version: int,
    tmp_dir: str,
    username: str,
    password: str,
    ) -> bool:
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
        token = fdm_login(fdm_ip, fdm_port, api_version, tmp_dir, username, password)
    try:
        fa = open("{}/token".format(tmp_dir), "r")
        token = fa.readline()
        fa.close()
    except:
        token = fdm_login(fdm_ip, fdm_port, api_version, tmp_dir, username, password)
    if token.count(".") == 2:
        result = True
    else:
        result = False
    return result
