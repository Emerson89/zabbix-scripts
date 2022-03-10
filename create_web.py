#!/usr/bin/python3
# Autor: Emerson Cesario
# E-mail: emerson.cesario50@gmail.com

from tabnanny import check
from zabbix_api import ZabbixAPI,Already_Exists
import sys
import getpass
import time
import csv

URL = sys.argv[1]
USERNAME = sys.argv[2]
PASSWORD = getpass.getpass("Password: ")

try:
    zapi = ZabbixAPI(URL, timeout=15)
    zapi.login(USERNAME, PASSWORD)
    print(f'Conectado na API do Zabbix, Versao Atual {zapi.api_version()}')
    print ()
except Exception as err:
    print(f'Falha ao conectar na API do zabbix, erro: {err}')

def procura_groups(hosts_ids):
     geral = zapi.host.get({
        "output": ['host','hostid'],
        "sortfield": "name",
        "search": {"name": '*' + hosts_ids + '*'},
        "searchWildcardsEnabled": True
     })
     print("***Host(s) encontrado(s)***")
     print()
     for x in geral:
        print(x['host'])
     print()
hosts_ids = input("Pesquise o o nome do host: ")
procura_groups(hosts_ids)

def procura_grupo(grupos):
     gethosts = input("Digite o nome do host que deseja incluir as Urls: ")
     grupos = zapi.host.get({
        "output": 'extend',
        "filter": { "name": [gethosts]},
        "selectHosts": ["name","host"],
     })[0]['hostid']
     print()
     return grupos

def create_web(nome, urlpass):
    try:
       create_web = zapi.httptest.create({
           "name": "Web check",
           "hostid": procura_grupo(grupos=''),
           "steps": [
            {
                "name": nome,
                "url": urlpass,
                "status_codes": "200",
                "no": 1
            },]
       })
 
       print(f'URL cadastrada {nome}')
    except Already_Exists:
       print(f'URL(s) já cadastrada {nome}')
    except Exception as err:
       print(f'Falha ao cadastrar URL {err}')

with open('urls.csv') as file:
    file_csv = csv.reader(file, delimiter=';')
    for [nomes,urls] in file_csv:
        create_web(nome=nomes,urlpass=urls)

zapi.logout()