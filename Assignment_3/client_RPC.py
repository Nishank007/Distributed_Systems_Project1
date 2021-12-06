import socket

HOST = '127.0.0.1'          # Use localhost
PORT = 5000                 # The server port the client will connect to

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Establish initial connection
server.connect((HOST, PORT))

# helper function for converting a string into bytes
def convert_to_bytes(string):
    return bytes(string, encoding="ascii")

def send_to_server(procedure):
    # Synchronously send request to the server
    print('Sending procedure to server')
    procedure_bytes = convert_to_bytes(procedure)
    server.send(procedure_bytes)

    print('Waiting for response from the server...')
    result = server.recv(1024).decode()
    if result:
        print('Result: ', result)

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
