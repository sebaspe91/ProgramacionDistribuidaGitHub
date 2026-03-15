# ProgramacionDistribuidaGitHub
Para realizar en calse y actividades independientes

# ¿Qué es cliente-servidor?
  El modelo cliente-servidor es una arquitectura de red donde los clientes (dispositivos o aplicaciones como navegadores web) solicitan recursos, datos o servicios, y   los servidores (equipos potentes centralizados) procesan dichas solicitudes y proporcionan la respuesta. Permite la administración centralizada de recursos,           mejorando   la eficiencia y seguridad al separar las tareas.
  
  Cliente: Es el usuario final o la aplicación que inicia la solicitud (navegador, app móvil, programa de escritorio).
  
  Servidor: Es una computadora o software potente que aloja datos, aplicaciones o recursos, escucha peticiones, las procesa y envía una respuesta.
  
  Red: El medio (internet o red local) por el cual se comunican.

# Diferencia entre proceso e hilo
Un proceso es un programa en ejecución con su propia memoria independiente, mientras que un hilo (thread) es una unidad de ejecución "ligera" dentro de un proceso que comparte recursos (memoria, archivos) con otros hilos del mismo proceso. Los procesos son más pesados y aislados, mientras que los hilos permiten ejecución concurrente más rápida dentro de una misma aplicación.

Memoria: Cada proceso tiene su propio espacio de memoria. Los hilos comparten la memoria del proceso padre.

Recursos: Los procesos consumen más recursos del sistema; los hilos son ligeros y consumen menos.

Independencia: Los procesos son independientes; si uno falla, no afecta a otros. Los hilos son dependientes; si un hilo falla gravemente, puede afectar al proceso entero.

Comunicación: La comunicación entre procesos (IPC) es lenta y compleja. La comunicación entre hilos es rápida y directa.

Ejemplo: Abrir el navegador Chrome es un proceso. Cada pestaña nueva dentro de Chrome es un hilo que comparte memoria.

# Que hizo
Se realizo una conexion con base a socket de dos archivos configurados como cliente y servidor en archivos.py, despues se modifico los mensjes de salida

# Que aprendio
Aprendi a realizar una conexion por medio de socket y su configuracion para la ejecucion, el despliegue y cual debe ser primero para el consumo del servidor

# Dificultades
El gitHub por medio de token no conocia ni manejaba bien esta herramienta todo muy manual
