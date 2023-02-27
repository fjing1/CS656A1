import sys
import socket
import os


def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('', 0))
        ip_addr, free_port = s.getsockname()
        return free_port
    #try/finally block to ensure that the socket is always closed, even if an exception is raised:
    finally:
        s.close()


def main():
    # Check command line arguments
    if len(sys.argv) != 6:
        print("Error: client input sys argument is not 5")
        return
    # type check parameters
    try:
        server_addr = str(sys.argv[1])
        n_port = int(sys.argv[2])
        mode = str(sys.argv[3])
        req_code = int(sys.argv[4])
        file_received = str(sys.argv[5])
    except ValueError:
        print('Error: check type of parameters')

    r_port = get_free_port()
    print("r_port (range 1025-65535):", r_port)
    # create udp socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # negotiation request
    nego_request = "PORT {} {}\r\n.format(server_addr, r_port)"
    # Create a TCP/IP socket
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        #active mode
        if mode == "a":

            # Connect to the server
            tcp_sock.connect((server_addr, n_port))

            # Send the PORT request with the port number and request code
            port_request = f"PORT {r_port} {req_code}"
            tcp_sock.send(port_request.encode())





    finally:
        # Clean up the socket
        tcp_sock.close()


if __name__ == '__main__':
    main()
