# Assignment 2 (Multi threaded server)

1. Start the server => "python3 multithread_server.py"
2. Start multiple clients on multiple terminals => "python3 client.py"
3. The file OPERATIONS to be performed are given below

	- Client reads from and stores files in the "/client_files" folder
	- Server reads from and stores files in  the "/server_files" folder

OPERATIONS:
1. Rename a file => "rename file_name.txt new_file_name.txt"
	// Checks "/server_files" folder for the file
2. Delete a file => "delete file_name.txt"
	// Checks "/server_files" folder for the file
3. Upload a file => "upload file_name.txt"
	// Checks "/server_files" folder for the file
4. Download a file => "download file_name.txt"
	// Check "/client_files" folder for the file

# References
https://www.geeksforgeeks.org/socket-programming-multi-threading-python/