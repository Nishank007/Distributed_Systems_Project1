# Assignment 3 (Synchronous RPC)

1. Start the server => "python3 server_RPC.py"
2. Start the client => "python3 client_RPC.py"

OPERATIONS:
1. Implement Matrix Multiplication
	- Type => "matrix_multiply(matrixA, matrixB, matrixC)"
 	- Example: matrix_multiply([[12,7,3], [4,5,6], [7,8,9]], [[5,8,1,2], [6,7,3,0], [4,5,9,1]], [[1,8,1,2], [6,7,3,0], [4,5,9,1]])
 	- Result: [[1314, 2332, 1134, 288], [948, 1636, 1022, 221], [1509, 2611, 1598, 350]]

2. Implement Add
 	- Type => "add(x,y)"
 	- Example: add(4,4)
 	- Result: 8

3. To Sort an Array
	- Type => "sort([n1,n2,n3])"
	- Example: sort([7,3,-2,13,0,5])
  	- Result: [-2, 0, 3, 5, 7, 13]

4. To calculate the value of Pi
  	- Type => "calculate_pi()"
  	- Result: 3.14159265359

# References
https://docs.python.org/3/howto/sockets.html#creating-a-socket