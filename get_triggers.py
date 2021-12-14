#!/usr/bin/python3
# Autor: Emerson Cesario
# E-mail: emerson.cesario50@gmail.com


from zabbix_api import ZabbixAPI
import csv
import sys
import getpass

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

ids = []

def procurando_triggers(hosts):
    ids = zapi.trigger.get({
        "output": ['triggerid','description'],
        "sortfield": "hostname",
        "search": {"hostname": '*' + hosts + '*'},
        "searchWildcardsEnabled": True
    })
    if ids:
        print("***Encontrados***")
        print()
        for x in ids:
            with open('hostsids.csv', 'a',newline='') as arquivo_csv:
               escrever = csv.writer(arquivo_csv, delimiter=';')
               escrever.writerow([x['triggerid'],x['description']])
            print (x['triggerid'],"-", x['description'])            
    else:
        print("***Hosts não encontrado***")
hosts = input("Pesquise o hostname: ")
print()
procurando_triggers(hosts)

zapi.logout()