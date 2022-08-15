/*****************************************************
** Program: smallsh.c
** Author: Mark Matamoros
** Date: November 11, 2017
** Description: Program 3
*****************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <signal.h>
#include <sys/wait.h>


//handler for ^c - from lecture
void catchSIGINT(int sigVal)
{
   if (WIFSIGNALED(sigVal) != 0)
   {
      //grab signal value from termination
      int termSignal = WTERMSIG(sigVal);

      //notify user
      printf("terminated by signal %d\n", termSignal);
      fflush(stdout);
   }
}

int main()
{
   int inputCharNum = -5;	//amount of characters inputted
   char* inputtedChars = NULL;	//address of inputted characters
   size_t bufferSize = 2048;	//size allocated for buffer

   char* token = NULL;		//hold tokens when parsing user input
   char* stringTokens[512];     //array of pointers for token holding
   int tokenLocation = 0;       //token location within array

   char *inputFile = NULL;      //string for directing input
   char *outputFile = NULL;     //string for directing output
   int fileInput = -5;		//for stream pointing in child
   int fileOutput = -5;         //for stream pointing in child
   int backgroundFlag = 0;      //signify a background process was requested (&)

   pid_t childPID = -5;		//hold child process' pid
   int exitMethod;              //for holding child's exit method
   int status = 0;              //for exiting status number 

   //intializize struct
   struct sigaction sa = {0};

   sa.sa_handler = catchSIGINT;
   sigfillset(&sa.sa_mask);
   sigaction(SIGINT, &sa, NULL);

   //input loop for processing and commands
   while(1)
   {
      //prompt user input
      printf(": ");
      fflush(stdout);

      //grab char input from user and remove "\n"   
      inputCharNum = getline(&inputtedChars, &bufferSize, stdin);

      //handle blank line
      if (inputtedChars[0] == '\n')
      {
         //printf("blank line test\n");
      }
      //handle commenting line
      else if (inputtedChars[0] == '#')
      {
         //printf("# key test\n");
      }
      else
      {
         //grab first token from input
         token = strtok(inputtedChars, " \n");

         //loop through char input and parse into an array
         while(token != NULL)
         {
            //for reading
            if (strcmp(token, "<") == 0)
            {
               //grab next token from user input
               ////stackoverflow.com/questions/42035420/how-do-i-get-the-second-token-from-a-single-string
               token = strtok(NULL, " \n");
             
               //copy token into input string variable
               //stackoverflow.com/questions/8056146/breaking-down-string-and-storing-it-in-array/change to home directory	 
               inputFile = strdup(token);
   
               //grab next token from user input for next loop iteration
               token = strtok(NULL, " \n");
            }  
            //for outputting
            else if (strcmp(token, ">") == 0)
            {
               //grab next token from user input
               token = strtok(NULL, " \n");

               //copy token into output string variable
               outputFile = strdup(token);

               //grab next token from user input for next loop iteration
	       token = strtok(NULL, " \n");
            }
            //signal background process
            else if (strcmp(token, "&") == 0)
            {
               //set flag to indicate background process
               backgroundFlag = 1;

               //exit loop
               break;
            }
            else
            {    
               stringTokens[tokenLocation] = strdup(token);

	       //grab next token from user input
               token = strtok(NULL, " \n");

               //increment to next array location
               tokenLocation++; 
            }
         }

         //set last set location to NULL
         stringTokens[tokenLocation] = NULL;

         //handle exit commmand
         if(strcmp(stringTokens[0], "exit") == 0)
         {
            exit(0);
         }
         //handle directory changes
         else if (strcmp(stringTokens[0], "cd") == 0)
         {
            if(stringTokens[1] == NULL)
            {
               //set to home directory
               //www.tutorialspoint.com/c_standard_library/c_function_getenv.htm
               chdir(getenv("HOME"));
            }
            else
            {
               //change to new directory location
               //pubs.opengroup.org/onlinepubs/009695399/functions/chdir.html
               chdir(stringTokens[1]);
            }
         }
         //handle exit value on status request
         else if(strcmp(stringTokens[0], "status") == 0)
         {
            printf("exit value %d\n", status);
            fflush(stdout);
         }
         //handle all other commands
         else
         {
            childPID = fork();

            //new process handling
            switch(childPID)
            {
               case -1:
                  exit(1);
                  break;

               case 0:
                  //for reading from file - user inputted
                  if(inputFile != NULL)
                  {
	             //atempt to open file for reading
                     fileInput = open(inputFile, O_RDONLY);

		     //check for file opening errors and notify user if error exists
                     if(fileInput < 0)
                     {
                        printf("cannot open %s for input\n", inputFile);
                        fflush(stdout);
                        exit(1);
                     }
                     //redirect file descriptor for reading - from lecture
                     else
                     {  
                        dup2(fileInput, 0);	//redirect stdout stream
                        close(fileInput);	//close file
                     }
                  }
                  //for non specified file for input
                  else
                  {
                     fileInput = open("/dev/null", O_RDONLY);
 
                     //check for file opening errors and notify user if error exists
                     if(fileInput < 0)
                     {
                        printf("ccanot open file for input\n", inputFile);
                        fflush(stdout);
                        exit(1);
                     }
                     //redirect file descriptor for reading - from lecture
                     else
                     {
                        dup2(fileInput, 0);
                        close(fileInput);
                     }
                  }

                  //for writing to file
                  if(outputFile != NULL)
                  {
		     //attempt to open file writing/creating
                     fileOutput = open(outputFile, O_WRONLY | O_CREAT, S_IRUSR | S_IWUSR);

                     //check for file opening errors and notify user if error exists
                     if(fileOutput < 0)
                     {
                        printf("cannot open %s for output\n", outputFile);
                        fflush(stdout);
                        exit(1);
                     }
                     //redirect file descriptor for writing - from lecture 
                     else
                     {
                        dup2(fileOutput, 1);	//redirect stdin stream
                        close(fileOutput);	//close file
                     }
                  }

                  //attempt execution of command to replace program
                  execvp(stringTokens[0], stringTokens);
                  
                  //if unable to execute, notify user and exit
                  printf("%s: no such file or directory\n", stringTokens[0]);
                  fflush(stdout);
                  exit(1);
                  
                  break;

               default:
                  //process is not set for background
                  if (backgroundFlag == 0)
                  {
                     //block parent until specified child process terminates 
                     waitpid(childPID, &exitMethod, 0);

                     //for normal exit 
                     if (WIFEXITED(exitMethod))
                     {
                        //grab exit status number
                        status = WEXITSTATUS(exitMethod);    
                     }
                  }
                  //process is set to background
                  else
                  {
                     printf("background pid is %d\n", childPID);
                     fflush(stdout);
                  }
                  break;
             }
         }

         //check if process has completed - from lecture
         childPID = waitpid(-1, &exitMethod, WNOHANG);
    
         //if pid exists
         if (childPID > 0)
         {
            //for normal exit
            if (WIFEXITED(exitMethod))
            { 
               //grab exit status number
               status = WEXITSTATUS(exitMethod);

               //notify user of background process exit and status value
               printf("background pid %d is done: exit value %d\n", childPID, status);
            }         
         }

         //clear the array of tokens for next iteration of user input
         for (int i = 0; i < 10; i++)
         {
            stringTokens[i] = NULL;
         }

         //reset token location
         tokenLocation = 0;

         //reset background flag
         backgroundFlag = 0;

         //clear input/output strings
         inputFile = NULL;
         outputFile = NULL;

      }
   }

   return 0;
}

