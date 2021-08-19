#!/usr/bin/python3

from zabbix_api import ZabbixAPI
import csv
import sys
import getpass

URL = input("Digite a URL Zabbix-server: ")
USERNAME = input("Digite usuário: ")
PASSWORD = getpass.getpass("Digite a senha: ")

try:
    zapi = ZabbixAPI(URL, timeout=15)
    zapi.login(USERNAME, PASSWORD)
    print(f'Conectado na API do Zabbix, Versao Atual {zapi.api_version()}')
    print ()
except Exception as err:
    print(f'Falha ao conectar na API do zabbix, erro: {err}')

ids = []

def procurando_hosts(group_ids):
    ids = zapi.hostgroup.get({
        "output": ['name','groupid'],
        "sortfield": "name",
        "search": {"name": '*' + group_ids + '*'},
        "searchWildcardsEnabled": True
    })
    if ids:
        print("***Groups encontrados***")
        print()
        for x in ids:
            with open('hostsids.csv', 'a') as arquivo_csv:
               escrever = csv.writer(arquivo_csv, delimiter=';')
               escrever.writerow([x['name'],x['groupid']])
            print (x['name'],"-", x['groupid'])            
    else:
        print("***Groups não encontrados***")
group_ids = input("Pesquise o CD do cliente: ")
print()
procurando_hosts(group_ids)

zapi.logout()