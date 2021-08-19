#!/usr/bin/python3

from zabbix_api import ZabbixAPI
import csv
import sys
import getpass

URL = input("Digite a URL Zabbix-server: ")
USERNAME = input("Digite seu usuário: ")
PASSWORD = getpass.getpass("Digite a sua senha: ")

try:
    zapi = ZabbixAPI(URL, timeout=15)
    zapi.login(USERNAME, PASSWORD)
    print(f'Conectado na API do Zabbix, Versao Atual {zapi.api_version()}')
    print ()
except Exception as err:
    print(f'Falha ao conectar na API do zabbix, erro: {err}')

def update_id(group, id):
    try:
        update_id = zapi.hostgroup.update({
            "name": group,
            "groupid": id 
        })

        print(f'Grupo atualizado {group}')
    except Exception as err:
        print(f'Falha ao atualizar {err}')
   
with open('hostsids.csv') as file:
    file_csv = csv.reader(file, delimiter=';',lineterminator='\n')
    for [groups,ids] in file_csv:
        update_id(group=groups,id=ids)

zapi.logout()