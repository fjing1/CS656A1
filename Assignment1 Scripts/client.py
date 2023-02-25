import sys
import socket

if len(sys.argv) != 6:
    print(f"Usage: {sys.argv[0]} <server_address> <n_port> <mode> <req_code> <file_received>")
    sys.exit(1)

server_address = sys.argv[1]
n_port = int(sys.argv[2])
mode = sys.argv[3]
req_code = int(sys.argv[4])
file_received = sys.argv[5]

try:
    # create socket for server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.settimeout(1.0)
    server_socket.connect((server_address, n_port))
except socket.error as err:
    print(f"Error connecting to server: {err}")
    sys.exit(1)

# send the request code to server
server_socket.sendall(str(req_code).encode())

# receive the status message from server
status_msg = server_socket.recv(1024).decode()
if status_msg != "OK":
    print(f"Server returned error: {status_msg}")
    sys.exit(1)

# send the mode to server
server_socket.sendall(mode.encode())

# receive the file content from server
file_content = server_socket.recv(1024).decode()

# save the file to disk
with open(file_received, "w") as f:
    f.write(file_content)

# close the socket
server_socket.close()

print("File downloaded successfully!")
