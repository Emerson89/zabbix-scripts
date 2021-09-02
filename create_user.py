#!/usr/bin/python3
# Autor: Emerson Cesario
# E-mail: emerson.cesario50@gmail.com

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

def procurando_groupusers(group_ids):
    ids = zapi.usergroup.get({
        "output": ['name','usrgrpid'],
        "sortfield": "name",
        "search": {"name": '*' + group_ids + '*'},
        "searchWildcardsEnabled": True
    })
    if ids:
        print("***GroupsUsers encontrados***")
        print()
        for x in ids:
            print (x['name'],"-", x['usrgrpid'])            
    else:
        print("***GroupsUsers não encontrados***")
group_ids = input("Pesquise o nome do grupo de usuario: ")
print()
procurando_groupusers(group_ids)
print()
GROUPID = input("Insira o groupid...: ")
print()
time.sleep(2)
print()

def create_user(user, password):
    try:
       create_user = zapi.user.create({
           "alias": user,
           "passwd": password,
           "usrgrps": [{"usrgrpid":GROUPID}],
       })
 
       print(f'User cadastrado {user}')
    except Already_Exists:
       print(f'User(s) já cadastrado {user}')
    except Exception as err:
       print(f'Falha ao cadastrar user {err}')

with open('users.csv') as file:
    file_csv = csv.reader(file, delimiter=';')
    for [nome,senha] in file_csv:
        create_user(user=nome,password=senha)

zapi.logout()