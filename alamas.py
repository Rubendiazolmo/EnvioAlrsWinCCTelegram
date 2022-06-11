import pandas as pd
import numpy as np
import sys
import string
import time
import subprocess
import json

PATH = "C:/Python/"

# Configuración de lectura de alarmas

COLUMNA_TEXTOS = "N" #Columna en la que está el texto que queremos enviar
INDEX_TEXTO    = string.ascii_lowercase.index(COLUMNA_TEXTOS.lower())
AlrAct         = sys.argv[1].replace("./Alrs/","") # Alarma activada, estructura pszMsgData de WinCC
AlrAct         = AlrAct.split("_")
AlrId          = int(AlrAct[0])
AlrStado       = int(AlrAct[1]) # 1 = Activada, 2 = Desactivada, 3 = Reconocida

# Configuración de avisos por telegram

TOKEN_BOT      = ""
CHAT_ID        = ""
MENSAJE_ALARMA = ""

# Lectura de alarmas desde Excel exportado

Alrs = np.array(pd.read_excel(PATH + 'Export.xlsx', sheet_name="Avisos"))[2:] #Extaigo los textos de las alarmas del Excel exportado en Wincc. Quito las 3 primeras filas del Excel para que sea más cómodo recorrer la matriz con un for.
Alrs = pd.DataFrame(Alrs)

for i, Alr in enumerate(Alrs[0]):
    
    if (Alr == (AlrId)) and (AlrStado == 1):
        MENSAJE_ALARMA = (str(Alrs[INDEX_TEXTO][i]) + " activada")
    if (Alr == (AlrId)) and (AlrStado == 2):
        MENSAJE_ALARMA = (str(Alrs[INDEX_TEXTO][i]) + " desactivada")

if MENSAJE_ALARMA != "":

    # Enviar mensaje y guardar respuesta de curl.
    rsp = subprocess.Popen(f'curl -d "text={MENSAJE_ALARMA}" -X POST https://api.telegram.org/bot{TOKEN_BOT}/sendMessage?chat_id={CHAT_ID}', stdout=subprocess.PIPE)
    stdout = json.load(rsp.stdout)
    
    ok = (stdout["ok"]) # Comprobar que el mensaja ha sido enviado
    
    #Si el mensaje no se ha enviado (por cualquier motivo a excepción del cooldown de Telegram) escribimos en log.txt la respuesta de curl y salimos del script con código de respuesta 1 (error)
    if not ok:
        print("El mensaje no se ha enviado")
        codigo_error = int(stdout["error_code"]) # Obtener código de error
        
        # Si el error no viene del cooldown guardo en el registro el error.
        if error_code != 429:
            log = open("log.txt", "a")
            log.write(str(time.time())+": "+str(stdout)+"\n")
            log.close()
        sys.exit(1)
    

time.sleep(0.75)
