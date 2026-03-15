# ACTIVIDAD CLASE
import threading
import time

lock = threading.Lock()


# variable gloabal
asientos = 10


def reservar():

    global asientos

    with lock:
        if asientos > 0:
            asientos -= 1
        print(f"Asiento # {asientos}")
    



for i in range(50):

    threading.Thread(target=reservar).start()

