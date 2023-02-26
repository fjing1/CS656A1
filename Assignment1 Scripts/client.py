import sys
import socket
import os


def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # tcp connection
        s.bind(('', 0))
        ip_addr, free_port = s.getsockname()  # return (ip address, port)
        # print(free_port)
        return free_port


def main():
    # Check command line arguments
    if len(sys.argv) != 5:
        print(f"Usage: {sys.argv[0]} <server_addr> <n_port> <mode> <req_code>")
        return

    server_addr = sys.argv[1]
    n_port = int(sys.argv[2])
    r_port = get_free_port()
    print("r_port:", r_port)
    mode = sys.argv[3]
    req_code = int(sys.argv[4])
    # create udp socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # negotiation request
    nego_request = "PORT {} {}\r\n.format(server_addr, r_port)"
    # Create a TCP/IP socket
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        server_addr = (server_addr, n_port)
        tcp_sock.connect(server_addr)
        print(f"Connected to {server_addr}")

        if mode == "p":
            # Passive mode: receive the file from the server
            file_data = tcp_sock.recv(1024)
            with open('received.txt', 'wb') as f:
                f.write(file_data)
            print("File received and saved as 'received.txt'")

        elif mode == "a":
            # Active mode: send the request code to the server and receive the file
            # converts req_code integer to 4-byte array of bytes in big-endian byte order

            PORT_data = req_code.to_bytes(4, byteorder='big') + r_port.to_bytes(4, byteorder='big')
            tcp_sock.sendall(PORT_data)
            # Receive the file from the server
            file_data = tcp_sock.recv(1024)
            with open('received.txt', 'wb') as f:
                f.write(file_data)
            print("File received and saved as 'received.txt'")

    finally:
        # Clean up the socket
        tcp_sock.close()


if __name__ == '__main__':
    main()
