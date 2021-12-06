#!/usr/bin/env python3

import socket
import os

HOST = '127.0.0.1'          # Use localhost
PORT = 5000                 # The server port the client will connect to

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Establish initial connection
server.connect((HOST, PORT))

# Helper function for converting string into bytes """
def convert_to_bytes(string):
    return bytes(string, encoding="ascii")


def download(file_path):
    server.settimeout(0.5)  # Timeout after waiting for a second
    f_path = open(file_path, 'wb')
    while True:
        try:
            data = server.recv(1024)

        except socket.timeout as e:
            if e.args[0] == 'timed out':
                print('File transfer is now complete')
                break
        else:
            f_path.write(data)
    f_path.close()
    print('File downloaded successfully')
    server.settimeout(None)  # Reset timeout


def request_download(args):
    # Send a download request to the server
    print('Requesting file download from server...')
    string = args[0] + ' ' + args[1]
    command = convert_to_bytes(string)
    server.send(command)

    # Wait for the server to acknowledge request
    print('Waiting for server to acknowledge request...')
    response = server.recv(1024).decode()  # ToDo => Assuming one buffer is enough

    if response == 'ok':
        file_path = 'client_files/' + args[1]
        print('Request accepted. Starting the download...')
        download(file_path)

    else:
        print('Download request denied with error: ', response)


def upload(file_path):
    """ Upload file to server """
    print('Starting upload to server...')
    f_path = open(file_path, 'rb')
    data = f_path.read(1024)
    while(data):
        server.send(data)
        data = f_path.read(1024)
    f_path.close()
    print('Upload complete!')


def request_upload(args):
    # Check if file is present in the client
    if len(args) == 2:
        file_path = 'client_files/' + args[1]

        if os.path.exists(file_path):
            print('Requesting the server to accept file...')
            string = args[0] + ' ' + args[1]
            command = convert_to_bytes(string)
            server.send(command)

            # Wait for the server to acknowledge request
            print('Waiting for server to acknowledge request...')
            response = server.recv(1024).decode()

            if response == 'ok':
                print('Request accepted.')
                upload(file_path)

            else:
                print('Upload request denied. Error: ', response)
        else:
            print('Missing file. Ensure the file is in the client_files folder')
    else:
        print('Invalid request. Usage: client.py [file_name]')

# Responds to the client request to rename a file
def rename(args):
    print('Requesting server to rename file...')
    if len(args) == 3:
        string = args[0] + ' ' + args[1] + ' ' + args[2]
        command = convert_to_bytes(string)
        server.send(command)
        response = server.recv(1024).decode()

        if response == 'ok':
            print('Rename successful')
        else:
            print('Rename request failed: ', response)
    else:
        print('Needs two arguments: client.py rename [inital_name] [new_name]')

# Responds to a client request to delete a file from the server
def delete(args):
    print('Requesting server to delete file...')
    string = args[0] + ' ' + args[1]
    command = convert_to_bytes(string)
    print("command before sending", command)
    server.send(command)

    response = server.recv(1024).decode()

    if response == 'ok':
        print('File deleted successfully')
    else:
        print('Delete request denied with error:', response)


def main():
    command = input()
    args = command.split(' ')

    if len(args) >= 2:
        operation = args[0]

        if operation == 'delete':
            delete(args)
        elif operation == 'rename':
            print('Renaming!')
            rename(args)
        elif operation == 'download':
            print('Downloading!')
            request_download(args)
        elif operation == 'upload':
            print('Uploading!')
            request_upload(args)
        else:
            print('Operation Invalid. Valid: upload, download, delete & rename')

    else:
        print('Must have at least 2 arguments. See Readme for details')

    print()
    print()


if __name__ == '__main__':
    while True:
        main()
    server.close()
