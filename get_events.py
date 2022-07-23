#!/usr/bin/python3
# Autor: Emerson Cesario
# E-mail: emerson.cesario50@gmail.com


from zabbix_api import ZabbixAPI
import csv
import sys
import getpass
from datetime import datetime


URL = sys.argv[1]
USERNAME = sys.argv[2]
PASSWORD = sys.argv[3]

try:
    zapi = ZabbixAPI(URL, timeout=15)
    zapi.login(USERNAME, PASSWORD)
    print(f'Conectado na API do Zabbix, Versao Atual {zapi.api_version()}')
    print ()
except Exception as err:
    print(f'Falha ao conectar na API do zabbix, erro: {err}')

ids = zapi.event.get({
        "output": ['clock','name','value','severity']
    })

severidades = [
    'Não classificada',
    'Informação',
    'Média',
    'Atenção',
    'Alta',
    'Desastre'
]

for event in ids:
    hora_evento = datetime.fromtimestamp(
        int(event['clock'])).strftime('%Y-%m-%d %H:%M:%S')
    severidade = severidades[(int(event['severity']))]
    print(severidade)
    print(
        'Evento: ' + event['name'] + ', ocorrido em: ' + hora_evento + ' com severidade ' + severidade)
    
zapi.logout()