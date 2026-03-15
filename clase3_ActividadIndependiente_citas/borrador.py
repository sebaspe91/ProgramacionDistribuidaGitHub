from datetime import datetime, timedelta, date

fecha_actual = datetime.now().strftime("%Y-%m-%d-%H:%M")

print(fecha_actual)

ano, mes, dia, hora = fecha_actual.split('-')

print(ano)
print(mes)
print(dia)
print(hora)