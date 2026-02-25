
import socket
import threading

# ejercicio en clase
import time

# contador del cliente
contador_clientes = 0  # recurso compartido
lock = threading.Lock()

def handle_client(conn, addr):
    
    global contador_clientes
    
    student_name = conn.recv(1024).decode()
    
    # section critica protegida
    with lock:   # with ==> con Lock es para saber cuando se ejecuta
        # Incrlemento contador
        contador_clientes += 1
        numero = contador_clientes

    print(f"Cliente {numero} atencion desde {addr}")

    time.sleep(10) # probar el tiempo delay

    response = f"Hola {student_name}, eres el cliente nuemro {numero}"
    conn.sendall(response.encode())
    
    conn.close()
    


# Aca empiza el codigo

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5000))
server.listen()

print("Servidor concurrente con lock...")

while True:
    conn, addr = server.accept()
    
    # crate a thread per client
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
# conn.close()
