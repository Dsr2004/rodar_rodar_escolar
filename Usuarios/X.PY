import mygeotab 
from datetime import datetime, timedelta
import pandas as pd
api = mygeotab.API(username='telematicarodar@gmail.com', password='Rodaryrodar2021*', database='rodaryrodar')
api.authenticate()
Fecha_Leida = datetime.now() + timedelta(hours=5)
ano = Fecha_Leida.year
mes = Fecha_Leida.month
dia = str(Fecha_Leida.day)
if len(dia) == 1:
    dia = "0" + dia
hora = str(Fecha_Leida.hour)
if len(hora) == 1:
    hora = "0" + hora
minuto = str(Fecha_Leida.minute)
if len(minuto) == 1:
    minuto = "0" + minuto
segundo = str(Fecha_Leida.second)
if len(segundo) == 1:
    segundo = "0" + segundo
savetime = str(ano) + '-' + str(mes) + '-' + str(dia) + 'T' + str(hora) + ':' + str(minuto) + ':' + str(
    segundo) + ".000Z"
# devices = api.call('Get', typeName = 'Device')
# devices = api.call('Get', typeName = 'Device', search={"licensePlate":"DFRL43"})
# Id_Buscado=devices[0]['id']
devices = api.call('Get', typeName='Device')
logs = api.get("LogRecord", search={"fromDate": savetime})
# logs = api.get("LogRecord", search = {"fromDate": savetime,"deviceSearch": {"id":'bA'}})
longitud = []
latitud = []
Fecha = []
ID = []
hora = []
##########INICIA MODIFICACIONES#########################################
placas = []
Id_Dive = []
for i in range(len(devices)):
    placas.append(devices[i]['licensePlate'])
    Id_Dive.append(devices[i]['id'])
for i in range(len(logs)):
    longitud.append(logs[i]['longitude'])
    latitud.append(logs[i]['latitude'])
    Fecha.append((logs[i]['dateTime'] - timedelta(hours=5)).date())
    hora.append((logs[i]['dateTime'] - timedelta(hours=5)).time().strftime('%H:%M:%S'))
    ID.append(logs[i]['device']['id'])
df_placa = pd.DataFrame({'ID': Id_Dive, 'Placa': placas})
df = pd.DataFrame({'ID': ID, 'longitud': longitud,
                    'latitud': latitud,
                    'Fecha': Fecha, 'Hora': hora
                    })
# Se realiza joiner de las dos tablas
df_cd = pd.merge(df, df_placa, how='inner', on='ID')
df_cd = df_cd.drop(['ID'], axis=1)
# Se coloca Df como se espera guardar
df = df_cd.rename(columns={'Placa': 'ID'})
df['latitud'][1]
df['longitud'][1]
df['ID'][1]

print(df)