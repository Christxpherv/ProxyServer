from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerPort = 8888
tcpSerSock = socket(AF_INET, SOCK_STREAM) #SOCK_STREAM indicates TCP socket

#bind the server socket and start listening
tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen(1)

while 1:
    # Start receiving data from the client
    print( 'Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print ('Received a connection from:', addr)
    message = tcpCliSock.recv(2048)
    if str( message, encoding='utf8' ) != '':
        print (message)

    # Extract the filename from the given message
        print (message.split()[1])
        file1 = str( message, encoding='utf8' )
        filename = file1.split()[1].split("/")[1]
        print (filename)
        fileExist = "false"
        filetouse = "/" + filename
        print (filetouse)
        try:
        # Check whether the file exist in the cache
            f = open(filetouse[1:], "rb")
            outputdata = f.readlines()
            fileExist = "true"

        # ProxyServer finds a cache hit and generates a response message
        
            tcpCliSock.send(bytes("HTTP/1.0 200 OK\r\n",'utf-8'))
            tcpCliSock.send(bytes("Content-Type:text/html\r\n",'utf-8'))
            for i in range(0, len(outputdata)):
                tcpCliSock.send(outputdata[i])
            f.close()
            print ('Read from cache')

    # Error handling for file not found in cache
        except IOError:
            if fileExist == "false":
            # Create a socket on the proxy server
                c = socket(AF_INET, SOCK_STREAM)
                hostn = filename.replace("www.", "", 1)
                print (hostn)
                try:
                # Connect to the socket to port 80
                    c.connect((hostn,80))
                    print('Socket connected to port 80 of the host')
            
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                    fileobj = c.makefile('rwb')
                    string1 = "GET " + "http://" + filename + " HTTP/1.0\n\n"
                    naming = bytes(string1,'utf-8')
                    c.send(naming)
                    fileobj.write(naming)
               
                # Read the response into buffer
                    buff = fileobj.readlines() # read all the files to the buffer
                
               
                
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                    tmpFile = open("./" + filename,"wb")
                    for i in range(0, len(buff)):
                        tmpFile.write(buff[i])
                        tcpCliSock.send(buff[i])
                
                    tmpFile.close()
                except:
                        print ("Illegal request")
            else:
            # HTTP response message for file not found
                
                print("File not Found")

    # Close the client and the server sockets
    tcpCliSock.close()
    
tcpSerSock.close()