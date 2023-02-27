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
    global req_code
    if len(sys.argv) != 3:
        print("check number of argument failed")
        exit(-1)
    # check req_code be int
    try:
        req_code = int(sys.argv[1])
        # print("Error: req_code should be an integer.")
    except ValueError:
        print("Error:sys.argv[1]/<req_code> must be int")

    file_to_send = sys.argv[2]
    # configure udp socket
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to a specific port
    server_address = ('', 0)
    udp_sock.bind(server_address)

    # Print the port number the server is listening on
    print("stage1 Negotiation using udp, <n_port>:", udp_sock.getsockname()[1])
    #prepare for stage 2
    # Create a TCP/IP socket
    s_tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        # Wait for a connection
        # print('stage1 Negotiation Server is waiting for a connection...')
        data, client_address = udp_sock.recvfrom(1024)  # max 1024 bytes
        print("Received data:", data, " from client_address", client_address)
        data = data.decode()
        data = data.split("|")
        print("data", data)
        client_req_code = int(data[2])
        if data[0] == "PORT":
            if client_req_code == req_code:
                # register r_port and send 1
                ack = 1
                r_port = int(data[1])
                # print(r_port)
                udp_sock.sendto(str(ack).encode(), client_address)
                # transition stage to r_port of client
                client_address_t = (client_address[0],r_port)
                s_tcp_sock.connect(client_address_t)
                #load the file
                with open('sent.txt', 'rb') as f:
                    file_data = f.read()
                try:
                    # send the file data
                    s_tcp_sock.sendall(file_data)
                finally:
                    # close the connection
                    s_tcp_sock.close()


            else:
                # send 0
                ack = 0
                #print(ack)
                udp_sock.sendto(str(ack).encode(), client_address)



        #elif data[0] == "PASV":

        # decode data
        """
         try:
            if not data:
                print("No data received")
                break
        """
        # client_req_code = int.from_bytes(data, byteorder='big')
        # print("Received request code: client_req_code:", client_req_code)

        # stage2


        # Listen for incoming connections
        # tcp_sock.listen(1)

        # finally:
        # Clean up the connection
        #    udp_sock.close()
        #    print("Connection closed\n")


if __name__ == '__main__':
    main()
