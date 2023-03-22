import pandas as pd
import numpy as np 

import happybase
import csv


def getConn():
    return happybase.Connection(host='localhost', port=9090)

connection=getConn()

#Si al conectar da el error -> thriftpy2.transport.base.TTransportException: TTransportException(type=1, message="Could not connect to ('0.0.0.0', 9090)")
#ejecutar en una terminal: hbase thrift start -p 9090

#funcion auxiliar para convertir a bytes lo que queremos almacenar en HBase
def to_bytes(value):
  return bytes(str(value), 'utf-8')
# Nombre del namespace que se va a crear
table_name = 'mbd10_30:airport'

# Familias de columnas que se van a crear
column_families = {
    'airport': dict(),
}

#try:
connection.create_table(table_name, column_families)
print(f'Tabla {table_name} creada en el namespace mbd10_30')
# except happybase.hbase.thriftpy2.hbase_thrift.AlreadyExists:
    #print(f'Tabla {table_name} ya existe en el namespace {namespace_name}')

# Abrir el archivo CSV
with open('/tmp/nosql/airData/airports.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    # Ignorar la primera línea (cabeceras)
    next(csvreader)

    # Para cada línea en el archivo CSV, insertar un registro en la tabla HBase
    with connection.table(table_name).batch(batch_size=1000) as table:
        for row in csvreader:
            # La primera columna "iata" se usará como la clave de fila en HBase
            row_key = to_bytes(row[0])

            # Los datos de cada columna se almacenarán en la familia de columnas correspondiente
            data = {
                'airport:name': to_bytes(row[1]),
                'airport:city': to_bytes(row[2]),
                'airport:state': to_bytes(row[3]),
                'airport:country': to_bytes(row[4]),
                'airport:lat': to_bytes(row[5]),
                'airport:long': to_bytes(row[6]),
            }

            # Insertar el registro en la tabla HBase
            table.put(row_key, data)


# Cerrar la conexión
connection.close()
