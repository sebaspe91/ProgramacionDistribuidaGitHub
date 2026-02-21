
import socket
import threading

def handle_client(conn, addr):
    print(f"Cliente conectado dede {addr}")

    try:
        student_name = conn.recv(1024).decode()
        response = f"Hola {student_name}, estas conectado a un servidor concurrente"
        conn.sendall(response.encode())
    except Exception as e:
        print(f"Error con {addr}: {e}")
    finally:
        conn.close()
        print(f"Conexion cerrada con {addr}")



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5000))
server.listen()

print("Servidor concurrente escuchando...")

while True:
    conn, addr = server.accept()

    # crate a thread per client
    client_thread = threading.Thread(
        target=handle_client,
        args=(conn, addr)
    )


    client_thread.start()
# conn.close()
