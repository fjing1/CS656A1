import sys
import socket
import os


# -*- coding: utf-8 -*-

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # tcp connection
        s.bind(('', 0))
        ip_addr, free_port = s.getsockname()  # return (ip address, port)
        # print(free_port)
        return free_port


# get_free_port()
def main():
    # Check command line arguments
    if len(sys.argv) != 3:
        print("check number of argument failed")
        exit(-1)
    # check req_code be int
    if not sys.argv[1].isdigit():
        print("Error: req_code should be an integer.")
        return
    req_code = int(sys.argv[1])

    file_to_send = sys.argv[2]
    # udp socket
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Create a TCP/IP socket
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific port
    server_address = ('', 0)
    tcp_sock.bind(server_address)

    # Print the port number the server is listening on
    print("Port numer the server is listening on ", tcp_sock.getsockname()[1])

    # Listen for incoming connections
    tcp_sock.listen(1)

    while True:
        # Wait for a connection
        print('Waiting for a connection...')
        connection, client_address = tcp_sock.accept()
        print("Accepted connection from client_address", client_address)

        try:
            # Receive the request code from the client
            data = connection.recv(4)
            if not data:
                print("No data received")
                break

            client_req_code = int.from_bytes(data, byteorder='big')
            print("Received request code: client_req_code:", client_req_code)

            if client_req_code != req_code:
                print("Invalid request code")
                connection.sendall(b"Invalid request code")
                break

            # Send the file to the client
            with open(file_to_send, 'rb') as f:
                file_data = f.read()
                connection.sendall(file_data)

            print("File", file_to_send, "sent to client")

        finally:
            # Clean up the connection
            connection.close()
            print("Connection closed\n")


if __name__ == '__main__':
    main()
