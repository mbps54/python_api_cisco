FROM centos/python-38-centos7:20210726-fad62e9

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY --chown=1001 ./api_fdm/ /api_fdm/
RUN  chmod +x /api_fdm/snmp_config_fdm.py
RUN  chmod +x /api_fdm/start.sh

WORKDIR /api_fdm

ENTRYPOINT ["/bin/bash", "start.sh"]