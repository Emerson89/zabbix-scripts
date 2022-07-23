#!/usr/bin/python3
# Autor: Emerson Cesario
# E-mail: emerson.cesario50@gmail.com

<<<<<<< HEAD
from email.mime import application
from zabbix_api import ZabbixAPI,Already_Exists
import csv
import sys
import getpass

URL = sys.argv[1]
USERNAME = sys.argv[2]
PASSWORD = getpass.getpass("Digite a senha: ")
=======
from tabnanny import check
from zabbix_api import ZabbixAPI,Already_Exists
import sys
import getpass
import time
import csv

URL = sys.argv[1]
USERNAME = sys.argv[2]
PASSWORD = getpass.getpass("Password: ")
>>>>>>> c2c603edc9d11fb41d34bfdfeac62a3ba6391fbe

try:
    zapi = ZabbixAPI(URL, timeout=15)
    zapi.login(USERNAME, PASSWORD)
    print(f'Conectado na API do Zabbix, Versao Atual {zapi.api_version()}')
    print ()
except Exception as err:
    print(f'Falha ao conectar na API do zabbix, erro: {err}')

<<<<<<< HEAD
hostname = 'Monitoramento URL'
group = 'Monitoramento URL'

h = zapi.host.get({
    "filter": {"host": [hostname]},
})
hg = zapi.hostgroup.get({
    "filter": {'name': [group]}
})

if not h:
 if not hg:
  zapi.hostgroup.create({"name": group})   
  hg = zapi.hostgroup.get({
    "filter": {"host": [group]},
  })[0]['groupid']
  zapi.host.create({
     "groups": [{ "groupid": hg}],
     "host": hostname,
     "proxy_hostid": "0",
     "interfaces": {
         "type": 1,
         "main": 1,
         "useip": 1,
         "ip": "127.0.0.1",
         "dns": "",
         "port": "10050",
         "details": {
             "version": 2,
             "bulk": 1,
             "community": "{$SNMP_COMMUNITY}"
         }
     }
  })   

hostids = zapi.host.get({
    "output": "extend",
    "filter": {"host": [hostname]},
    "selectHosts": ["hostid", "host"]
    })[0]['hostid']


             
def create_web(step):         
        try:
           nome = "Web Check " + step
           try:
            a = zapi.application.get({"output": 'extend',
                                "hostid": hostids, 
                                "filter":{'name': "Web Check " +step}
                                })[0]['applicationid']
           except Exception as IndexError: 
            app = zapi.application.create({"name": "Web Check " +step,
                                "hostid": hostids})

            a = zapi.application.get({"output": 'extend',
                                "hostid": hostids, 
                                "filter":{'name': "Web Check " +step}
                                })[0]['applicationid']

           create_web = zapi.httptest.create({
              "name": "Web Check "+ step,
              "hostid": hostids,
              "applicationid": a,
              "steps": [
               {
                   "name": nome,
                   "url": step,
                   "status_codes": "200",
                   "no": 1
               }
              ]
           })
           
           trigger = zapi.trigger.create({"description": "Failed step of scenario URL: " + step,
                                "expression": "{"+hostname+":web.test.fail["+nome+"].sum(#3)}>=3",
                                "hostid": hostids,
                                "priority": 5})
           
           print(f'URL(s) cadastrada {r}')
        except Already_Exists:
           print(f'URL(s) já cadastrada {r}')
        except Exception as err:
           print(f'Falha ao cadastrar a URL(s) {err}')

with open('urls.csv') as file:
    file_csv = csv.reader(file, delimiter=';')
    for [r] in file_csv:
        create_web(step=r)

zapi.logout()
   
=======
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
>>>>>>> c2c603edc9d11fb41d34bfdfeac62a3ba6391fbe
