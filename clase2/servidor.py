
import socket
import threading

# contador del cliente
contador_clientes = 0  # recurso compartido
lock = threading.Lock()

def handle_client(conn, addr):

    global contador_clientes

    student_name = conn.recv(1024).decode()

    while lock:
        # Incrlemento contador
        contador_clientes += 1
        numero = contador_clientes

    print(f"Cliente {numero} atenido desde {addr}")
        
    response = f"Hola {student_name}, eres el cliente nuemro {numero}"
    conn.sendall(response.encode())

    conn.close()




server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5000))
server.listen()

print("Servidor concurrente con lock...")

while True:
    conn, addr = server.accept()

    # crate a thread per client
    client_thread = threading.Thread(
        target=handle_client, 
        args=(conn, addr)
    )

    client_thread.start()
# conn.close()
