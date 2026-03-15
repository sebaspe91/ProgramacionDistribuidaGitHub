# ACTIVIDAD CLASE
import threading


# variable gloabal
cursos = 10


def reservarCursos():

    global cursos

    for i in range(50):
        if cursos > 0:
            cursos -= 1
        print(f"Curso sin lock # {cursos}")
    



for i in range(50):

    threading.Thread(target=reservarCursos).start()
