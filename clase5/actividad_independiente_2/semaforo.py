import threading
import time

sem = threading.Semaphore(3)

# variable gloabal
cursos = 10


def reservarCursos():

    global cursos

    sem.acquire()
    time.sleep(3)
    if cursos > 0:
        cursos -= 1

    print(f"El curso con semaforo esta {cursos}")

    sem.release()


for i in range(50):

    threading.Thread(target=reservarCursos).start()
