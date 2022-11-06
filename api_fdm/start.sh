#!/bin/bash
if [ -z ${FDM_IP+foo} ]; then
exec python3 /api_fdm/snmp_config_fdm.py
else
exec python3 /api_fdm/snmp_config_fdm.py \
--fdm_ip $FDM_IP \
--username $USERNAME \
--password $PASSWORD \
--snmp_server_ip $SNMP_SERVER_IP \
--snmp_user $SNMP_USER \
--snmp_host_name $SNMP_HOST_NAME \
--auth_key $AUTH_KEY \
--encr_key $ENCR_KEY \
--interface_name $INTERFACE_NAME \
--deploy $DEPLOY \
--fdm_port $FDM_PORT \
--api_version $API_VERSION
fi