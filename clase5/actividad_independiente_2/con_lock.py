# ACTIVIDAD CLASE
import threading
import time

lock = threading.Lock()


# variable gloabal
cursos = 10


def reservarCursos():

    global cursos

    with lock:
        if cursos > 0:
            cursos -= 1
        print(f"Curso con lock # {cursos}")
    



for i in range(50):

    threading.Thread(target=reservarCursos).start()
