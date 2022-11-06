#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import click
from typing import Union
from functions.fdm_post import fdm_post
from functions.fdm_post_np import fdm_post_np
from functions.fdm_get import fdm_get
from functions.initial_auth import initial_auth
from functions.basic_functions import get_items_from_group
from functions.basic_functions import check_for_errors
from functions.basic_functions import jijna2_to_json


@click.command()
@click.option('--fdm_ip', prompt=True, type=str, required=True, help='Cisco FDM management IP')
@click.option('--username', prompt=True, type=str, required=True, help='Cisco FDM username')
@click.option('--password', prompt=True, type=str, required=True,  hide_input=True, help='Cisco FDM password')
@click.option('--snmp_server_ip', prompt=True, type=str, required=True, help='SNMP server IP')
@click.option('--snmp_host_name', prompt=True, type=str, required=True, help='Object name for SNMP server IP')
@click.option('--snmp_user', prompt=True, type=str, required=True, help='SNMP username')
@click.option('--auth_key', prompt=True, type=str, required=True, hide_input=True, help='SNMP SHA authentication key')
@click.option('--encr_key', prompt=True, type=str, required=True, hide_input=True, help='SNMP AES 128 encryption key')
@click.option('--interface_name', prompt=True, type=str, required=True, help='Cisco FDM interface for SNMP')
@click.option('--deploy', prompt=True, type=bool, default=False, help='Deploy config now or not')
@click.option('--fdm_port', type=str, default='443', help='Cisco FDM management port')
@click.option('--api_version', type=str, default='6', help='Cisco FDM API version')
@click.option('--tmp_dir', type=str, default='tmp', help='Temp directory for script')
@click.option('--offset', type=str, default='0', help='Offset for JSON')
@click.option('--limit', type=str, default=0, help='MAX object output')
def play(
    fdm_ip: str,
    fdm_port: str,
    api_version: str,
    username: str,
    password: str,
    snmp_server_ip: str,
    snmp_user: str,
    auth_key: str,
    encr_key: str,
    interface_name: str,
    snmp_host_name: str,
    tmp_dir: str,
    offset: str,
    limit: str,
    deploy: bool,
    ) -> Union[dict, str]:

    values = {
        'snmp_host_name': snmp_host_name,
        'snmp_server_ip': snmp_server_ip,
        'snmp_user': snmp_user,
        'auth_key': auth_key,
        'encr_key': encr_key,
    }
    if deploy == "True":
        deploy = True
    elif deploy == "False":
        deploy = False

    ### STEP-1: AUTHENTICATION
    auth = initial_auth(fdm_ip, fdm_port, api_version, tmp_dir, username, password)
    if not auth:
        sys.exit()

    ### STEP-2: CREATE OBJECT NETWORK
    api_path = 'object/networks'
    payload = jijna2_to_json('object_networks.txt', values)
    object_networks_info = fdm_post(
        fdm_ip, fdm_port, api_version, api_path, payload, tmp_dir, username, password
    )

    ### STEP-3: CREATE SNMP USER
    api_path = 'object/snmpusers'
    payload = jijna2_to_json('object_snmpusers.txt', values)
    object_snmpusers_info = fdm_post(
        fdm_ip, fdm_port, api_version, api_path, payload, tmp_dir, username, password
    )

    ### STEP-4: GET INTERFACE DATA
    api_path = 'devices/default/interfaces'
    devices_default_interfaces_info = fdm_get(
        fdm_ip, fdm_port, api_version, api_path, tmp_dir, username, password
    )
    interface_info = get_items_from_group(
        devices_default_interfaces_info, interface_name
    )

    ### STEP-5: CREATE SNMP HOST
    api_path = 'object/snmphosts'
    results_list = [object_networks_info, object_snmpusers_info, interface_info]
    success = check_for_errors(results_list)

    if success:
        gathered_values = {
            'object_networks_version': object_networks_info['version'],
            'object_networks_name': object_networks_info['name'],
            'object_networks_id': object_networks_info['id'],
            'object_networks_type': object_networks_info['type'],
            'object_snmpusers_version': object_snmpusers_info['version'],
            'object_snmpusers_name': object_snmpusers_info['name'],
            'object_snmpusers_id': object_snmpusers_info['id'],
            'object_snmpusers_type': object_snmpusers_info['type'],
            'interface_version': interface_info['version'],
            'interface_name': interface_info['name'],
            'interface_id': interface_info['id'],
            'interface_type': interface_info['type'],
        }
        payload = jijna2_to_json('object_snmphosts.txt', gathered_values)
        object_snmphosts_info = fdm_post(
            fdm_ip,
            fdm_port,
            api_version,
            api_path,
            payload,
            tmp_dir,
            username,
            password,
        )
        result = json.dumps(object_snmphosts_info, indent=2, sort_keys=True)
    else:
        result = 'Not all requests are successful'

    ### STEP-6: DEPLOY
    if success and deploy == True:
        api_path = 'operational/deploy'
        result = fdm_post_np(
        fdm_ip, fdm_port, api_version, api_path, tmp_dir, username, password
        )

    ### END
    print('\nSUMMARY:\n', result)
    return result


if __name__ == '__main__':
    result = play()