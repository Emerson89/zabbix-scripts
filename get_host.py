#!/usr/bin/python3

from zabbix_api import ZabbixAPI
import csv
import sys
import getpass

URL = sys.argv[1]
USERNAME = sys.argv[2]
PASSWORD = getpass.getpass("Digite a senha: ")

try:
    zapi = ZabbixAPI(URL, timeout=15)
    zapi.login(USERNAME, PASSWORD)
    print(f'Conectado na API do Zabbix, Versao Atual {zapi.api_version()}')
    print ()
except Exception as err:
    print(f'Falha ao conectar na API do zabbix, erro: {err}')

ids = []

def procurando_hosts(host_ids):
    ids = zapi.host.get({
        "output": ['host','hostid', 'description'],
        "sortfield": "name",
        "search": {"name": '*' + host_ids + '*'},
        "searchWildcardsEnabled": True
    })
    if ids:
        print("***Hosts encontrados***")
        print()
        for x in ids:
            with open('hostsids.csv', 'a') as arquivo_csv:
               escrever = csv.writer(arquivo_csv, delimiter=';')
               escrever.writerow([x['host'],x['hostid'],x['description']])
            print (x['host'],"-", x['description'])            
    else:
        print("***Hosts não encontrado***")
host_ids = input("Pesquise o CD do cliente: ")
print()
procurando_hosts(host_ids)

zapi.logout()