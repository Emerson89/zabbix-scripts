#!/usr/bin/python3

from zabbix_api import ZabbixAPI
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

def procurando_hosts(host_ids):
    ids = zapi.host.get({
        "output": ['host','hostid'],
        "sortfield": "name",
        "search": {"name": '*' + host_ids + '*'},
        "searchWildcardsEnabled": True
    })
    if ids:
        print("***Hosts encontrados***")
        print()
        for x in ids:
            print (x['host'],"-", x['hostid'])            
    else:
        print("***Hosts não encontrados***")

while True:

      print("Escolha uma opção:\n1 - Remove host\n2 - Sair")
      opcao = input()
      if opcao == "1":
       host_ids = input("Pesquise o CD ou hostname do cliente: ")
       print()
       procurando_hosts(host_ids)
       print()
       HOST = input("Insira o hostid do host...: ")
       print()
       zapi.host.delete([HOST])
       print(f'***Host removido do zabbix {HOST}***')
       print()
      elif opcao == "2":
          break

zapi.logout()