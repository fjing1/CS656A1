import sys
import socket
import os


def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("", 0))
        ip_addr, free_port = s.getsockname()
        return free_port
    # try/finally block to ensure that the socket is always closed, even if an exception is raised:
    finally:
        s.close()


def main():
    # Check command line arguments
    if len(sys.argv) < 6:
        print(
            "Error: Expect 5 parameters <server_address>, <n_port>, <mode>, <req_code>,  <file_received> "
        )
        return

    # type check parameters
    try:
        server_addr = str(sys.argv[1])
        n_port = int(sys.argv[2])
        mode = str(sys.argv[3])
        req_code = int(sys.argv[4])
        file_received = str(sys.argv[5])
    except ValueError:
        print("Error: check type of parameters")
    # stage 1. Negotiation using UDP sockets
    r_port = get_free_port()
    print("r_port (range 1025-65535):", r_port)
    # create udp socket
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # depends on the mode:
    if mode == "A":
        # need to send PORT <r_port> <req_code>
        PORT_msg = "PORT" "|"+ str(r_port)+"|" + str(req_code)
        print(PORT_msg.encode(), (server_addr, n_port))
        udp_sock.sendto(PORT_msg.encode(), (server_addr, n_port))# default encode is UTF-8

    elif mode == "P":
        print("P")

    data, client_address = udp_sock.recvfrom(1024)  # max 1024 bytes
    print("C received data:", data, " from server_addr", client_address)
    data = data.decode()
    # receive r_port from server

    # Create a TCP/IP socket
    # tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


if __name__ == "__main__":
    main()
