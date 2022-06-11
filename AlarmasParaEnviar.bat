@echo off

REM Compruebo que no se está ejecutando el script en otro proceso.
REM Bloquear la ejecución de scripts de wincc no lo veo viable, cuando hay muchas alarmas en cola para enviar, puede llegar a tardar mucho tiempo.
if not exist "C:\Python\Enviando" (

REM Creo un archivo para ver que se está ejecutando el script (Si hay muchas alarmas en cola, la ejecución puede tardar lo suyo en enviar todas las alarmas)
echo Enviando > C:\Python\Enviando

REM Si el script no se está ejecutando en otro proceso paso el nombre de cada archivo como parámetro de entrada al Script de Python y si el código de respusta
REM del script es 0 (ejecución correcta) borro el archivo que se ha pasado al script.
tasklist | findstr forfiles || forfiles /P C:\Python\Alrs /C "cmd /c python C:\Python\alarmas.py @file && del @file"

REM Borro el archivo auxiliar que utilizo para ver que se está ejecutando el script
del C:\Python\Enviando
)
