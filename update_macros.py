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
        print (x['hostmacroid'],"-",x['macro'],"-",x['value'])
nome_macros = input("Pesquise pelo id do host: ")
print()
procurando_macros(nome_macros)
print()

macros = input("Insira o macroid...: ")
new_macros = input("Insira um novo nome macro...:")
new_value = input("Insira um novo valor...:")

update_id = zapi.usermacro.update({
            "hostmacroid": macros,
            "macro": new_macros,
            "value": new_value
        })

print(update_id)

zapi.logout()
   