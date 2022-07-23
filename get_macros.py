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

def procurando_macros(nome_macros):
    id = zapi.usermacro.get({
        "output": "extend",
        "search": "hostids"
    })
    for x in id:
            with open('macros.csv', 'a',newline='') as arquivo_csv:
               escrever = csv.writer(arquivo_csv, delimiter=';')
               escrever.writerow([x['hostid'],x['value']])
nome_macros = input("Pesquise pelo id do host: ")
print()
procurando_macros(nome_macros)
print()

zapi.logout()
   