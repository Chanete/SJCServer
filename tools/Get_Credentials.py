#!/usr/bin/python3
import sys
sys.argv.append("--noauth_local_webserver")
sys.path.append('../')
import config
from yt_functions.yt_functions import get_authenticated_service
from oauth2client.tools import argparser

#
#
#
#    MAIN
#
#
#

if __name__ == "__main__":
      
# Definir los argumentos que recibie el programa      

  argparser.add_argument("--canal", help="Canal de emision (Interno o Camino)", required=True)
#  argparser.add_argument("--noauth_local_webserver", help="Authtype",    default=True)
  args = argparser.parse_args()
  canal=args.canal
  youtube = get_authenticated_service(canal,args)   # Conecta y autentica el API de Google
 