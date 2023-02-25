import sys
import socket
import os

def main():
    # Check command line arguments
    if len(sys.argv) != 5:
        print(f"Usage: {sys.argv[0]} <server_address> <n_port> <mode> <req_code>")
        return

    server_address = sys.argv[1]
    n_port = int(sys.argv[2])
    mode = sys.argv[3]
    req_code = int(sys.argv[4])

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        server_address = (server_address, n_port)
        sock.connect(server_address)
        print(f"Connected to {server_address}")

        if mode == "p":
            # Passive mode: receive the file from the server
            file_data = sock.recv(1024)
            with open('received.txt', 'wb') as f:
                f.write(file_data)
            print("File received and saved as 'received.txt'")

        elif mode == "a":
            # Active mode: send the request code to the server and receive the file
            sock.sendall(req_code.to_bytes(4, byteorder='big'))

            # Receive the file from the server
            file_data = sock.recv(1024)
            with open('received.txt', 'wb') as f:
                f.write(file_data)
            print("File received and saved as 'received.txt'")

    finally:
        # Clean up the socket
        sock.close()


if __name__ == '__main__':
    main()
