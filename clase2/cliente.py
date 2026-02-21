import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5000))

student_name = input("Ingrese tu nombre: ")
client.sendall(student_name.encode())

response = client.recv(1024).decode()

print(response)
# mensaje = client.recv(1024)
# print("Estudiante :", mensaje.decode())

client.close()
