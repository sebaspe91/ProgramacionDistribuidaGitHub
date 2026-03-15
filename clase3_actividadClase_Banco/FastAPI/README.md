
Preguntas:

•¿Es seguro usar variable global?

    NO, no es seguro en un entorno de producción con múltiples peticiones concurrentes

    # Ejemplo de problema de concurrencia:
        clientes = [{"id": 1, "nombre": "Ana"}]  # Variable global

        # Petición 1: DELETE /clientes/1
        # Petición 2: GET /clientes (al mismo tiempo)

        # Posible problema:
        # - Petición 1 empieza a eliminar pero no termina
        # - Petición 2 intenta leer mientras se está eliminando
        # - ¡Resultado impredecible!

•¿Dónde aparece el recurso compartido?

    El recurso compartido es la lista clientes

•¿Se debería usar lock en producción?

    Lo que hemos visto en clase es No usarlo mientras se usa "asyncio" ya que una usa los hilos para realizar multiples tareas y "lock" bloque todo hasta que termine la tarea