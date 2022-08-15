/************************************************************************************************
 ** Program Name: ftserver.c
 ** Author: Mark Matamoros
 ** Date: 8/10/2018
 ** Description: Project 2 - ftserver
 ** Testing Machine: flip1.engr.oregonstate.edu
 ************************************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>
#include <fcntl.h>
#include <dirent.h>

/*************************************************************************************************
 ** Function Name: addressInfoSetup
 ** Description: Set structs for socket creation and usage
 ** Input: server port number (char*)
 ** Output: linked list for addrinfo structs (addrinfo*)
 ** Ref:http://man7.org/linux/man-pages/man3/getaddrinfo.3.html
 ** Ref:https://beej.us/guide/bgnet/html/multi/syscalls.html
 ************************************************************************************************/
struct addrinfo* addressInfoSetup(char* serverPort)
{
    struct addrinfo hints;          //holds socket criteria
    struct addrinfo *serverInfo;    //holds linked list of structs for connection
    int status;                     //holds returning getaddrinfo value
    
    memset(&hints, 0, sizeof(hints));	//clear struct's memory
    hints.ai_family = AF_INET;          //version IPv4
    hints.ai_socktype = SOCK_STREAM;	//TCP
    hints.ai_flags = AI_PASSIVE;        //assign local host address
    
    //grab returning value to determine success (0)
    status = getaddrinfo(NULL, serverPort, &hints, &serverInfo);
    
    //for any unsuccessful returning values
    if (status != 0)
    {
        fprintf(stderr, "Address information error.\n");
        exit(1);
    }
    
    return serverInfo;
}

/*************************************************************************************************
 ** Function Name: addressInfoSetupForDataSocket
 ** Description: Set structs for data socket creation and usage
 ** Input: client address and requested port
 ** Output: linked list for addrinfo structs (addrinfo*)
 ** Ref:http://man7.org/linux/man-pages/man3/getaddrinfo.3.html
 ** Ref:https://beej.us/guide/bgnet/html/multi/syscalls.html
 ************************************************************************************************/
struct addrinfo* addressInfoSetupForDataSocket(char* clientAddress, char* dataPort)
{
    struct addrinfo hints;          //holds socket criteria
    struct addrinfo *serverInfo;    //holds linked list of structs for connection
    int status;                     //holds returning getaddrinfo value
    
    memset(&hints, 0, sizeof(hints));	//clear struct's memory
    hints.ai_family = AF_INET;          //version IPv4
    hints.ai_socktype = SOCK_STREAM;	//TCP

    //grab returning value to determine success (0)
    status = getaddrinfo(clientAddress, dataPort, &hints, &serverInfo);
   
    //for any unsuccessful returning values
    if (status != 0)
    {
        fprintf(stderr, "Address information error.\n");
        exit(1);
    }

    return serverInfo;
}

/*******************************************************************************************************
 ** Function Name: implementServerSocket
 ** Description: create and bind socket. set for listening.
 ** Input: linked list of addrinfo structs for server (addrinfo*)
 ** Output: socket file descriptor
 ** Ref:https://beej.us/guide/bgnet/html/multi/syscalls.html
 ** Ref:https://beej.us/guide/bgnet/html/multi/clientserver.html
 ** Ref:http://man7.org/linux/man-pages/man2/socket.2.html
 ******************************************************************************************************/
int implementServerSocket(struct addrinfo* serverInfo)
{
    int sockfd = 0;         //hold socket file descriptor
    int status;             //holds returning value
 
    //create socket and grab returning value
    sockfd = socket(serverInfo->ai_family, serverInfo->ai_socktype, serverInfo->ai_protocol);
    
    //check for unncessful return value ("-1": error)
    if (sockfd == -1)
    {
        fprintf(stderr, "Socket creation error.\n");
        exit(1);
    }

    //associate socket to port on server
    status = bind(sockfd, serverInfo->ai_addr, serverInfo->ai_addrlen);
    
    //check for unsuccessful return value ("-1": error)
    if (status == -1)
    {
        fprintf(stderr, "Socket binding error.\n");
        exit(1);
    }
    
    //set socket to listen for incoming messages (10 max for queue)
    status = listen(sockfd, 10);
    
    //check for unncessful return value ("-1": error)
    if (status == -1)
    {
        fprintf(stderr, "Socket listening error.\n");
        exit(1);
    }
    
    return sockfd;
}

/*******************************************************************************************************
 ** Function Name: implementDataSocket
 ** Description: create and connect data socket
 ** Input: linked list of addrinfo structs (addrinfo*)
 ** Output: socket file descriptor
 ** Ref:https://beej.us/guide/bgnet/html/multi/syscalls.html
 ** Ref:https://beej.us/guide/bgnet/html/multi/clientserver.html
 ** Ref:http://man7.org/linux/man-pages/man2/socket.2.html
 ******************************************************************************************************/
int implementDataSocket(struct addrinfo* serverInfo)
{
    int sockfd = 0;         //hold socket file descriptor
    int status;             //holds returning value

    //create socket and grab returning value
    sockfd = socket(serverInfo->ai_family, serverInfo->ai_socktype, serverInfo->ai_protocol);
    
    //check for unncessful return value ("-1": error)
    if (sockfd == -1)
    {
        fprintf(stderr, "Socket creation error.\n");
        exit(1);
    }
   
    //connect socket and grab returning value
    status = connect(sockfd, serverInfo->ai_addr, serverInfo->ai_addrlen);

    //check for unsuccessful return value ("-1": error, "0": okay)
    if (status == -1)
    {
        fprintf(stderr, "Socket connection error.\n");
        exit(1);
    }

    return sockfd;
}


/*******************************************************************************************************
 ** Function Name: clientRequests
 ** Description:
 ** Input:
 ** Output: none
 ** Ref: https://beej.us/guide/bgnet/html/multi/clientserver.html
 ** Ref: https://www.geeksforgeeks.org/c-program-list-files-sub-directories-directory/
 ** Ref: http://pubs.opengroup.org/onlinepubs/009604599/functions/opendir.html
 ** Ref: http://pubs.opengroup.org/onlinepubs/7990989775/xsh/readdir.html
 ******************************************************************************************************/
void clientRequests(int newSockfd)
{
    char clientAddress[16];         //holds client's IP address
    char flipNum[5];                //holds local flip number
    char dataPort[5];               //holds client's data port request
    char userRequest[5];            //holds client's command request
    
    struct addrinfo* serverInfo;    //store linked list of structs for data connection
    int dataSockfd;                 //store socket file descriptor for data connection
    
    //prep (clear) char array memory prior to receiving messages
    memset(clientAddress, 0, sizeof(clientAddress));
    memset(flipNum, 0, sizeof(flipNum));
    memset(dataPort, 0, sizeof(dataPort));
    memset(userRequest, 0, sizeof(userRequest));
    
    //receive client address, server (this one) flip w/ #, data port request, and user command
    recv(newSockfd, clientAddress, sizeof(clientAddress), 0);
    recv(newSockfd, flipNum, sizeof(flipNum), 0);
    recv(newSockfd, dataPort, sizeof(dataPort), 0);
    recv(newSockfd, userRequest, sizeof(userRequest), 0);
    
    printf("Connection from %s.\n", clientAddress);

    //compare user command to determine request (list directory)
    if(strcmp(userRequest, "l") == 0)
    {
        //holds directory info...
        //...and prep (clear) memory for transfer
        char directoryMessage[1000];
        memset(directoryMessage, '\0', sizeof(directoryMessage));
        
        printf("List directory requested on port %s.\n", dataPort);
        printf("Sending directory contents to %s:%s.\n", clientAddress, dataPort);
       
        //call function to setup structs for data socket creation and usage
        //store the result (linked list of structs)
        serverInfo = addressInfoSetupForDataSocket(clientAddress, dataPort);

        //call function to create and store data socket for transfer
        dataSockfd = implementDataSocket(serverInfo);
 
        //open directory stream and return pointer to DIR object
        DIR* dirStream = opendir(".");

        //pointer for directory entry
        struct dirent* dirEntry;

        //handle un-openable directory
        if (dirStream == NULL)
        {
            printf("Directory could not be opened.\n");
            exit(1);
        }
        
        //loop through entire directory
        while((dirEntry = readdir(dirStream)) != 0)
        {
            //concatenate message with each directory file
            //include a space in between each entry for easy separation in client python script
            strcat(directoryMessage, dirEntry->d_name);
            strcat(directoryMessage, " ");
        }
   
        //send message to client containing directory information
        send(dataSockfd, directoryMessage, strlen(directoryMessage), 0);
        
	//close direcotry stream and data socket
        closedir(dirStream);
        close(dataSockfd);
    }
    else if(strcmp(userRequest, "g") == 0)
    {
        char* fileName[20];	//holds requested file name
        int fileDescriptor; 	//file descriptor for opening

	//clear memory prior to recieving the requested file name
        memset(fileName, 0, sizeof(fileName));
        recv(newSockfd, fileName, sizeof(fileName), 0);

        //call function to setup structs for data socket creation and usage
        //store the result (linked list of structs
        //serverInfo = addressInfoSetupforDataSocket(clientAddress, dataPort);

        //call function to create and store data socket for transfer
        dataSockfd = implementDataSocket(serverInfo);

    }
    else
    {
        printf("User command error.\n");
    }
}

/*******************************************************************************************************
 ** Function Name: main
 ** Description: Handles socket creation and manages connections for client services
 ** Input: server port number
 ** Output: none
 ** Ref: https://beej.us/guide/bgnet/html/multi/clientserver.html
 ** Ref:https://www.ibm.com/support/knowledgecenter/en/SSLTBW_2.3.0/com.ibm.zos.v2r3.bpxbd00/accept.htm
 *******************************************************************************************************/
int main(int argc, char *argv[])
{
    struct addrinfo* serverInfo;            //holds server's info for connecting
    int sockfd;                             //holds socket file descriptor
    
    struct sockaddr_storage clientAddress;      //holds the client's address info
    socklen_t clientAddressSize;                //holds the size of the client's address
    clientAddressSize = sizeof(clientAddress);  //grab size of the sockaddr_storage struct
    int newSockfd;                              //holds new socket FD for client connection
    
    //check for correct argument count
    if(argc != 2)
    {
        fprintf(stderr, "Please enter a valid port argument");
        return 1;
    }

    //call function to setup structs for socket creation and usage
    //store the result (linked list of structs)
    serverInfo = addressInfoSetup(argv[1]);
    
    //create and bind socket; set for listening
    //after listening, store returning socket file descriptior
    sockfd = implementServerSocket(serverInfo);
    
    printf("Server open on %s\n", argv[1]);
    
    //loop handles connection and services for client
    while (1)
    {
        //accept client connection and return new socket file descriptor
        newSockfd = accept(sockfd, (struct sockaddr*)&clientAddress, &clientAddressSize);
        
        //check for unncessful return value ("-1": error)
        if (newSockfd == -1)
        {
            fprintf(stderr, "Socket error when connecting to client.\n");
            exit(1);
        }
        
        //handle client requests for file listings and transfers
        clientRequests(newSockfd);
        
        //close socket
        close(newSockfd);
    }
    
    //free linked-list of structs
    freeaddrinfo(serverInfo);
    
    return 0;
}
