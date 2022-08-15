#***********************************************************************************************
#* Program Name: ftclient.py
#* Author: Mark Matamoros
#* Date: 8/10/2018
#* Description: Project 2 - ftclient
#* Testing Machine: flip2.engr.oregonstate.edu
#************************************************************************************************

from socket import *
import sys

#***************************************************************************************************
#* Function: implementDataSocket
#* Description: create socket to recieve data messages from server
#* Input: None (looks at commandline arguments)
#* Output: socket object for data transfer
#* Ref:Lecture 15 (slides)
#* Ref:https://code.tutsplus.com/tutorials/introduction-to-network-programming-in-python--cms-30459
#* Ref:https://docs.python.org/3/library/socket.html
#***************************************************************************************************
def implementDataSocket():
    #grab correct argument (data port) dependent on user command
    if sys.argv[3] == "-l":
        dataPort = 4
    if sys.argv[3] == "-g":
        dataPort = 5

    #setup socket for data transfer
    portNumber = int(sys.argv[dataPort])           #store (correct) commandline port number
    dataSocket = socket(AF_INET, SOCK_STREAM)      #create IPv4/TCP Socket
    dataSocket.bind(('', portNumber))              #bind socket to local port
    dataSocket.listen(1)                           #listen for incoming TCP requests

    #accept connecting server
    #grab socket object and address
    connection, address = dataSocket.accept()

    return connection

#***************************************************************************************************
#* Function: implementServices
#* Description: Handles user requests for either directory listing or file transfers
#* Input: socket for server connection
#* Output: None
#* Ref:https://code.tutsplus.com/tutorials/introduction-to-network-programming-in-python--cms-30459
#* Ref:https://docs.python.org/3/library/socket.html
#* Ref:https://www.tutorialspoint.com/python3/string_split.htm
#***************************************************************************************************
def implementServices(mySocket):
    #grab my address/port (list) and store
    address = mySocket.getsockname()

    #grab IP address from list
    clientAddress = address[0]
    
    #send my IP address to the server
    mySocket.send(clientAddress.encode('utf_8'))
    
    #send (server) flip w/ Number to the server
    mySocket.send(sys.argv[1].encode('utf_8'))

    #handles directory list command
    if sys.argv[3] == "-l":
        #send requested data port number to server
        mySocket.send(sys.argv[4].encode('utf_8'))
        
        #send user command to server
        mySocket.send("l".encode('utf_8'))
        
        #setup port for server connection
        dataSocket = implementDataSocket()
        
        print("Receiving directory structure from " + sys.argv[1] + ":" + sys.argv[4])

        #recieve message containing director contents
        directory = dataSocket.recv(1000)

        #place files into array, dictated by space separations in message
        dirListing = directory.split()

        #loop through array and display individual files
        for dirFile in dirListing:
            print(dirFile.decode("utf-8"))	

        #close socket
        dataSocket.close()

    #handles file request
    if sys.argv[3] == "-g":
        #send requested data port number to server
        mySocket.send(sys.argv[5].encode('utf_8'))

        #send user command to server
        mySocket.send("g".encode('utf_8'))

        #send text file name to server
        mySocket.send(sys.arg[4]('utf_8'))

        #setup port for server connection
        dataSocket = implementDataSocket()

        print("Receiving " + sys.arg[4] + " from " + sys.argv[1] + ":" + sys.argv[5])



#***************************************************************************************************
#* Description: Main area for creating/connecting socket and implementing server requests
#* Input: server address, server port number, command, filename (optional), data port number
#* Output: None
#* Ref:https://code.tutsplus.com/tutorials/introduction-to-network-programming-in-python--cms-30459
#* Ref:https://docs.python.org/3/library/socket.html
#***************************************************************************************************

#check for valid amount of user arguments
if (len(sys.argv) != 5 and len(sys.argv) != 6):
    print ("Please enter a valid amount of arguments")
    exit(1)

#append commandline host name with OSU's engr address and store
serverName = sys.argv[1] + ".engr.oregonstate.edu"

#store commandline server port number
serverPort = int(sys.argv[2])

#create IPv4/UDP socket and connect with client
mySocket = socket(AF_INET, SOCK_STREAM)
mySocket.connect((serverName, serverPort))

#handle client requests
implementServices(mySocket)

mySocket.close()
