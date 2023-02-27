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

    #create the tcp connection now
    c_tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # depends on the mode:
    if mode == "A":
        # need to send PORT <r_port> <req_code>
        a_msg = "PORT" "|"+ str(r_port)+"|" + str(req_code)
        print(a_msg.encode(), (server_addr, n_port))

        c_tcp_sock.bind(('',r_port))
        # needs to listen before send
        c_tcp_sock.listen(1)

        #sending message via udp to server
        udp_sock.sendto(a_msg.encode(), (server_addr, n_port))# default encode is UTF-8
        data, client_address = udp_sock.recvfrom(1024)  # max 1024 bytes
        print("C received data:", data, " from server_addr", client_address)
        data = data.decode()

        file_data = b''
        while True:
            connectionSocket, addr = c_tcp_sock.accept()
            print("accepted")
            incoming_data = connectionSocket.recv(1024)
            print("incoming data",incoming_data)
            if not incoming_data:
                break
            file_data += incoming_data

        with open(file_received, 'wb') as f:
            f.write(file_data)


    elif mode == "P":
        p_msg = "PASV" "|"+ str(req_code)
        print(p_msg.encode(), (server_addr, n_port))
        udp_sock.sendto(p_msg.encode(), (server_addr, n_port))# default encode is UTF-8
        data, client_address = udp_sock.recvfrom(1024)  # max 1024 bytes
        print("C received data:", data, " from server_addr", client_address)
        data = data.decode()



    # receive r_port from server



if __name__ == "__main__":
    main()
