#!/bin/bash

# Obtener ruta absoluta del archivo .db
DB_PATH=$(realpath "$1")

# Forzar carga de librerías del sistema
export LD_LIBRARY_PATH="/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu"

# Ejecutar DB Browser con la base de datos
/usr/bin/sqlitebrowser "$DB_PATH" 2>&1 | tee /tmp/db_browser.log

# Verificar resultado
if [ $? -ne 0 ]; then
    echo -e "\nERROR: Verifique el log en /tmp/db_browser.log"
    exit 1
fi