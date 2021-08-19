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

def update_id(hosts, id, descript):
    try:
        update_id = zapi.host.update({
            "host": hosts,
            "hostid": id,
            "description": descript 
        })

        print(f'Host atualizado {hosts}')
    except Exception as err:
        print(f'Falha ao atualizar {err}')
   
with open('hostsids.csv') as file:
    file_csv = csv.reader(file, delimiter=';',lineterminator='\n')
    for [nome,ids,desc] in file_csv:
        update_id(hosts=nome,id=ids,descript=desc)

zapi.logout()