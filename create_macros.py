#!/usr/bin/python3
# Autor: Emerson Cesario
# E-mail: emerson.cesario50@gmail.com

from zabbix_api import ZabbixAPI,Already_Exists
import csv
import sys
import time

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

def create_macros(idhost, valor):
    try:
       create_macros = zapi.usermacro.create({
           "hostid": idhost,
           "macro": "{$SNMP_COMMUNITY}",
           "value": valor,
       })
 
       print(f'Macro cadastrada {idhost}')
    except Already_Exists:
       print(f'Macro(s) já cadastrada {idhost}')
    except Exception as err:
       print(f'Falha ao cadastrar a macro {err}')

with open('macros.csv') as file:
    file_csv = csv.reader(file, delimiter=';')
    for [id,valores] in file_csv:
        create_macros(idhost=id,valor=valores)

zapi.logout()
   