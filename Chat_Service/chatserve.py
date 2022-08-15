#***********************************************************************************************
#* Program Name: chatserve.py
#* Author: Mark Matamoros
#* Date: 8/1/2018
#* Description: Project 1 - chatserve
#* Testing Machine: flip1.engr.oregonstate.edu
#************************************************************************************************

from socket import *
import sys

#***************************************************************************************************
#* Function: implementChat
#* Description: Handles sending of messages between server and client
#* Input: socket object (connection), user name (userName)
#* Output: None
#* Ref:Lecture 15 (slides)
#* Ref:https://stackoverflow.com/questions/13979764/python-converting-sock-recv-to-string
#* Ref:https://www.tutorialspoint.com/python3/python_networking.htm
#* Ref:https://docs.python.org/3/howto/unicode.html
#***************************************************************************************************
def implementChat(connection, userName):
    #recieve client name and store (change byte stream to utf-8)
    clientName = connection.recv(10).decode('utf-8')
    
    #send user name to client (encode string to byte stream)
    connection.send(userName.encode('utf-8'))
    
    #loop handles the receiving and sending of messages
    while 1:
        #recieve message and store (change byte stream to utf-8); remove newline
        receivedMessage = connection.recv(501).decode('utf-8')
        receivedMessage = receivedMessage.strip('\n')
        
        #check for "quit" message" and break (chat) loop or...
        if (receivedMessage == "\quit"):
            print("Connection closed.")
            break
        else:
        #output client message
            print("{}> {}".format(clientName, receivedMessage))

        #initilize message variable for message length loop
        sendingMessage = ""
        
        #check that message does not exceed 500 chars
        while len(sendingMessage) == 0 or len(sendingMessage) > 500:
            sendingMessage = input("{}> ".format(userName))

        #handle user request to quit (disconnect); break loop
        if (sendingMessage == "\quit"):
            print("Connection closed.")
            break
        
        #send message to client (encode string to byte stream)
        connection.send(sendingMessage.encode('utf-8'))

#***************************************************************************************************
#* Description: Main area for creating/connecting socket, creating user name,
#*   and implementing chat between both sides
#* Input: Commandline port #
#* Output: None
#* Ref:Lecture 15 (slides)
#* Ref:https://code.tutsplus.com/tutorials/introduction-to-network-programming-in-python--cms-30459
#* Ref:https://docs.python.org/3/library/socket.html
#***************************************************************************************************

#initialize user name variable for input/comparison
userName = ""

#check for proper argument count (port #)
if len(sys.argv) != 2:
    print ("Please enter a single port number argument")
    exit(1)

#Setup socket
myPort = sys.argv[1]                        #store commandline port number
mySocket = socket(AF_INET, SOCK_STREAM)     #create IPv4/UDP Socket
mySocket.bind(('', int(myPort)))            #bind socket to local port
mySocket.listen(1)                          #listen for incoming TCP Requests

#Prompt for user name input and check for max length (10)
while len(userName) > 10 or len(userName) == 0:
    userName = input("Please enter a username, 10 characters or less: ")

#loop handles server waiting for connection and chatting with connected client
while 1:
    print("Waiting for connection...")
    
    #accept connecting client
    #grab socket object and client's address
    connection, clientAddress = mySocket.accept()
    
    print("Connected to {}".format(clientAddress))
    
    #call chatting function
    implementChat(connection, userName)
    
    #close the connection
    connection.close()

