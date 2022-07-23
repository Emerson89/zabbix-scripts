#!/usr/bin/python3
# Autor: Emerson Cesario
# E-mail: emerson.cesario50@gmail.com

from doctest import testfile
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

test = input("dite:")

def create_macros(macros, values):
   
  try:
      create_macros = zapi.usermacro.create({
        "hostid": test,
        "macro": macros,
        "value": values
      })
      print(f'User cadastrado {macros}')
  except Already_Exists:
      print(f'User(s) já cadastrado {macros}')
  except Exception as err:
      print(f'Falha ao cadastrar user {err}')
 
with open('macros.csv') as file:
    file_csv = csv.reader(file, delimiter=';')
    for [macross,valores] in file_csv:
       create_macros(macros=macross,values=valores)       
    