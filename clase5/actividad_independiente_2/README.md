# Descripción del Problema

Imaginemos una plataforma educativa que ofrece 10 cursos. 50 usuarios intentan reservar un curso simultáneamente. Sin mecanismos de control de concurrencia, podrían producirse **condiciones de carrera (race conditions)** donde múltiples usuarios reserven el mismo curso, resultando en más reservas que cursos disponibles.

# Solucion con Lock:

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

# Solucion con Semaforo:

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


# Resultados esperados:

- Sin Lock: Quedarán varios cursos sin reservar correctamente (condición de carrera)

- Con Lock: Quedarán 0 cursos (reservas correctas)

- Con Semáforo: Quedarán 0 cursos (reservas correctas, pero máximo 3 simultáneas)