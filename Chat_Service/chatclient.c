/************************************************************************
** Program Name: chatserve.py
** Author: Mark Matamoros
** Date: 8/1/2018
** Description: Project 1 - chatserve
** Testing Machine: flip1.engr.oregonstate.edu
*************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>

/*************************************************************************
** Function Name: addressInfoSetup
** Description: Set structs for socket creation and usage
** Input: server host address (char*), port number (char*)
** Output: linked list for addrinfo structs (addrinfo*)
** Ref:http://man7.org/linux/man-pages/man3/getaddrinfo.3.html
** Ref:https://beej.us/guide/bgnet/html/multi/syscalls.html
*************************************************************************/
struct addrinfo* addressInfoSetup(char* serverHost, char* serverPort)
{
	struct addrinfo hints;          //holds socket criteria
	struct addrinfo *serverInfo;    //holds linked list of structs for connection
	int status;                     //holds returning getaddrinfo value

	memset(&hints, 0, sizeof(hints));	//clear struct's memory
	hints.ai_family = AF_INET;          //version IPv4
	hints.ai_socktype = SOCK_STREAM;	//TCP

    //grab returning value to determine success (0)
	status = getaddrinfo(serverHost, serverPort, &hints, &serverInfo);

    //for any unsuccessful returning values
	if (status != 0)
	{	
		fprintf(stderr, "Address information error.\n");
	 	exit(1);
	}

	return serverInfo;
}

/*************************************************************************
** Function Name: implementSocket
** Description: create and connect socket
** Input: linked list of addrinfo structs for server (addrinfo*)
** Output: socket file description (int)
** Ref:https://beej.us/guide/bgnet/html/multi/syscalls.html
** Ref:https://beej.us/guide/bgnet/html/multi/clientserver.html
** Ref:http://man7.org/linux/man-pages/man2/socket.2.html
** Ref:http://man7.org/linux/man-pages/man2/connect.2.html
**************************************************************************/
int implementSocket(struct addrinfo* serverInfo)
{
	int sockfd;     //holds returning socket file descriptor
    int status;     //holds returning value
    
    //create socket and grab returning value
	sockfd = socket(serverInfo->ai_family, serverInfo->ai_socktype, serverInfo->ai_protocol);

    //check for unncessful return value ("-1": error)
	if (sockfd == -1)
	{
		fprintf(stderr, "Socket creation error.\n");
        exit(1);
	}

    //connect socket to host and grab returning value
	status = connect(sockfd, serverInfo->ai_addr, serverInfo->ai_addrlen);

    //check for unncessful return value ("-1": error, "0": okay)
	if (status == -1)
	{
		fprintf(stderr, "Socket connection error.\n");
		exit(1);
	}
    
    return sockfd;
}

/*******************************************************************************
 ** Function Name: implementChat
 ** Description: Handles chatting, sending and receiving messages
 ** Input: socket file descriptor (int), user name (char*), server name (char*)
 ** Output: none
 ** Ref:https://beej.us/guide/bgnet/html/multi/syscalls.html
 *******************************************************************************/
void implementChat(int sockfd, char* userName, char* serverName)
{
    //arrays for holding message inputting and outputting
	char input[501];
	char output[501];

    //holds value for handling disconnection from server
    int status;
  
    //clear input and output messages' memory
	memset(input, 0, sizeof(input));
	memset(output, 0, sizeof(output));
    
    //send username to server
    send(sockfd, userName, strlen(userName), 0);
    
    //recieve server-side created name and store
    recv(sockfd, serverName, 10, 0);
    
    //grab new line character (clean output)
    getchar();
    
    //loop handles sending and receiving of messages
	while(1)
	{
        //output prompt containing username
        printf("%s> ", userName);
        
        //grab and store input
		fgets(input, 500, stdin);

        //compare user input for quitting command
		if (strcmp(input, "\\quit\n") == 0)
		{
            printf("Connection closed.\n");
            
            //send quitting command to server to notify connection termination
            send(sockfd, input, strlen(input), 0);
            
            close(sockfd);     //close socket
            
			exit(0);
		}

        //send user input to server
		send(sockfd, input, strlen(input), 0);

        //wait for server response; thereafter grab and store received message
        //grab returning value recv value (for connection termination)
		status = recv(sockfd, output, 500, 0);

        //check if server has closed the connection
		if(status == 0)
		{
			printf("Connection closed by server.\n");
            
            close(sockfd);      //close socket
            
            exit(0);
		}
        //print recieved server message
		else
		{
			printf("%s> %s\n", serverName, output);
		}

        //clear input and output messages' memory
		memset(input, 0, sizeof(input));
		memset(output, 0, sizeof(output));
	}
}

/*******************************************************************************
 ** Function Name: main
 ** Description: Handles user name input and function calling to create chat
 ** Input: Commandline entry - hostname and port number
 ** Output: none
 ** Ref:https://beej.us/guide/bgnet/html/multi/syscalls.html
 ** Ref:https://beej.us/guide/bgnet/html/multi/clientserver.html
 *******************************************************************************/
int main(int argc, char *argv[])
{
    char userName[11];      //hold user inputted name
    char serverName[10];    //hold server name
    int sockfd = 0;         //hold socket file descriptor
    
    //check for correct argument count
    if(argc != 3)
	{
		fprintf(stderr, "Please enter the valid host and port arguments");
		return 1;
	}

    //prompt user for name input with max length (10 char)
    printf("Please enter your name (10 characters max): ");
    scanf("%s", userName);
    userName[10] = '\0';        //terminate character string

    
    //call function to setup structs for socket creation and usage
    //store the result (linked list of structs)
	struct addrinfo* serverInfo = addressInfoSetup(argv[1], argv[2]);

    //call functiont to create and connect socket
    //store returning socket file descriptor
    sockfd = implementSocket(serverInfo);

    //call chat function
	implementChat(sockfd, userName, serverName);

	return 0;
}
