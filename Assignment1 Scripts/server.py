import sys
import socket
import os

def main():
    # Check command line arguments
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <req_code> <file_to_send>")
        return

    req_code = int(sys.argv[1])
    file_to_send = sys.argv[2]

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific port
    server_address = ('', 0)
    sock.bind(server_address)

    # Print the port number the server is listening on
    print(f"Starting up on {sock.getsockname()[1]}")

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        print('Waiting for a connection...')
        connection, client_address = sock.accept()
        print(f"Accepted connection from {client_address}")

        try:
            # Receive the request code from the client
            data = connection.recv(4)
            if not data:
                print("No data received")
                break

            client_req_code = int.from_bytes(data, byteorder='big')
            print(f"Received request code: {client_req_code}")

            if client_req_code != req_code:
                print("Invalid request code")
                connection.sendall(b"Invalid request code")
                break

            # Send the file to the client
            with open(file_to_send, 'rb') as f:
                file_data = f.read()
                connection.sendall(file_data)

            print(f"File '{file_to_send}' sent to client")

        finally:
            # Clean up the connection
            connection.close()
            print("Connection closed\n")


if __name__ == '__main__':
    main()
