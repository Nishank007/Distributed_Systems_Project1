#!/usr/bin/env python3

import socket
import os

HOST = '127.0.0.1'          # Use localhost
PORT = 5000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

 # Responds to the download request from the client
def download(args, conn):
    file_path = 'server_files/' + args[1]
    if os.path.exists(file_path):
        conn.send(b'ok')

        # sending file to the client
        f_path = open(file_path, 'rb')
        data = f_path.read(1024)
        while (data):
            conn.send(data)
            ldata = f_path.read(1024)
        f_path.close()
        print('Sending complete!')
    else:
        conn.send(b'File not found in server')

# Receive the uploaded file and save it to the server
def upload(file_path, conn):
    conn.settimeout(0.5)  # Timeout after waiting for a second
    f_path = open(file_path, 'wb')
    while True:
        try:
            data = conn.recv(1024)

        except socket.timeout:
            print('File transfer is now complete')
            break
        else:
            f_path.write(data)

    f_path.close()
    print('Successfully uploaded new file')
    conn.settimeout(None)  # Reset timeout

# Validate upload request from client
def request_upload(args, conn):
    print('Received upload request from a client')
    file_path = 'server_files/' + args[1]
    if os.path.exists(file_path):
        print('Upload request denied, file with the same name already exists')
        conn.send(b'File with the same name already exists')
    else:
        conn.send(b'ok')

        # waiting for the upload from the client
        upload(file_path, conn)


# Responds to the client request to rename a file
def rename(args, conn):
    print('Received rename request from a client')
    file_path = 'server_files/' + args[1]
    if len(args) == 3 and os.path.exists(file_path):
        src = file_path
        dest = 'server_files/' + args[2]
        # Rename the file
        os.rename(src, dest)
        print("File successfully renamed")
        print("Sending acknowledgment to client!")
        conn.send(b'ok')
    else:
        print("Rename request denied. Sending error to client")
        conn.send(b'File not found in server')

# Process request from client to delete file_name
def delete(args, conn):
    print('Received a delete request from a client')

    if len(args) == 2:
        file_path = 'server_files/' + args[1]
        print('file_path', file_path)
        if os.path.exists(file_path):
            print("Acknowledgment sent to client!")
            conn.send(b'ok')
            # Delete the file
            os.remove(file_path)
            print("File successfully deleted")
        else:
            print('File not found')
            conn.send(b'File not found')
    else:
        print("Delete request denied. Sending error to client")
        conn.send(b'Invalid delete request')


def main():
    conn, addr = server.accept()
    print("Just accepted a connection from ", addr)
    while True:
        request = conn.recv(1024).decode()
        if request:
            args = request.split()
            operation = args[0]
            print('operation', operation)

            if operation == 'delete':
                delete(args, conn)
            elif operation == 'rename':
                rename(args, conn)
            elif operation == 'download':
                download(args, conn)
            elif operation == 'upload':
                request_upload(args, conn)
            else:
                print('Server only supports upload, download, rename & delete.')

        print()
        print()

if __name__ == '__main__':
    main()
