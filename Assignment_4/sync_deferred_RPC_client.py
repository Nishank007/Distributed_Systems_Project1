#!/usr/bin/env python3

import socket
import time
import threading

HOST = '127.0.0.1'          # Use localhost
PORT = 5000                 # The server port the client will connect to

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Establish initial connection
server.connect((HOST, PORT))

# helper function for converting string into bytes
def convert_to_bytes(string):
    return bytes(string, encoding="ascii")

# Synchronously send request to the server
def send_to_server(procedure):
    print('Sending procedure to server')
    procedure_bytes = convert_to_bytes(procedure)
    server.send(procedure_bytes)

    print('Waiting for acknowledgement from the server...')
    ack = server.recv(1024).decode()
    if ack == 'ok':
        print('Received acknowledgement from the server')
        print('Proceeding to do other work until receives interruption from the server')
        interrupt_now = False
        do_stuff_thread = threading.Thread(target=do_stuff, args =(lambda : interrupt_now, ))
        do_stuff_thread.start()

        # Original thread waits for any interrupts from the server
        result = server.recv(1024).decode()
        interrupt_now = True
        do_stuff_thread.join()

        print("Successfully interrupted by the server!")
        print("Result", result)

    else:
        print('An error occured: ', ack)

# helper function to keep busy until we query for results
def do_stuff(interrupt_now):
    print('Doing stuff until interrupted by server')
    while True:
        print('Doing stuff...')
        if interrupt_now:
            break


def query_for_result():
    print('Querying the server for the result')
    query = 'query_result()'
    server.send(convert_to_bytes(query))

    # Get response
    response = s.recv(1024).decode()
    if response and response != 'invalid':
        print('Got result from the server')
        print('Result is: ', response)
    else:
        print('Server does not have the result')
        print('Response: ', response)


def main():     # The entry point for the server
    procedure = input()
    if procedure:
        send_to_server(procedure)

        print()
        print()


if __name__ == '__main__':
    while True:
        main()
    server.close()
