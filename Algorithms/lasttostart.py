#********************************************************************************************
# Program Name: lasttostart.py
# Author: Mark Matamoros
# Date: February 4, 2018
# Description: Homework Week 4 - Last to Start Example
#********************************************************************************************

#********************************************************************************************
# pull values from text and create a list containing lists
#********************************************************************************************

#create empty list for integer-list storage
listList = []

#open file for reading
with open("act.txt", 'r') as fileObject:
    
    #iterate through lines in file
    for line in fileObject:
        
        #create a list of numbers that were previously sepearated by whitespace
        tempList = line.split()
        
        #convert the number(strings) into integer values
        tempList = [int(number) for number in tempList]
        
        #add list to the "list of lists"
        listList.append(tempList)

#******************************************************************************************
# list manipulation for handling sorting and processing
#******************************************************************************************

#holds a 3-dimensional list
#1rst Dimension holds every activity from all sets
#2nd Dimension holds every activity from each set
#3rd Dimension each activity within each set
startFinishList = []

#holds the 2nd Dimension set's activities
tempSetList = []

#counter for dumping
i = -1

#loop through each set of numbers separated by line breaks
for x in range(0, len(listList)):
    
    #handles the case where the set's activity amount is listed
    if (len(listList[x]) == 1):
        
        #increment counter to activate dump (initially activates on second+ finding)
        i += 1
        
        #handles the dumping of the set's activities into 3-dimensional list
        if (i%2 == 1):
            startFinishList.append(tempSetList)
            
            #clear the set's activity list for future dumping
            tempSetList = []
            
            #increment counter for setting dump upon finding a set activity amount
            i += 1

    #handles the insertion of activities
    if (len(listList[x]) == 3):
        
        #insert activity into temporary set list of activities
        tempSetList.append(listList[x])

#dump the final set's activity list
startFinishList.append(tempSetList)

#***********************************************************************************************
# lastToStart: sorts a list of lists, where each list has an activity number, a start time,
#  and a finishin time.  The sorting is handled with an ascending start time order. Thereafter,
#  the sorted list is processed to locate compatible activities, where each activity's start time
#  does not overlap with a prior activity's end time. These compatible activity's indices are
#  stored
# paramaters: a list of lists (activities with three elements, mentioned in the description)
# algorithm reference: lecture
#***********************************************************************************************
def lastToStart(list):

    #returning list that holds a compatible set of activities
    compatibleList = []

    #sort list in order of ascending start times (2nd element)
    #REF: https://docs.python.org/2/howto/sorting.html
    tempList = sorted(list, key=lambda x: (x[1]))

    #set length accordingly for "for" loop
    listLength = len(tempList) - 1
    
    #set variable to the first compatible element
    compatibleIndex = listLength

    #store the first (in this case, last) element to the returning compatible list,
    #as the greedy algorithm will always intially utilize the last element
    compatibleList.append(tempList[compatibleIndex][0])

    #loop through (in a decreasing manner) the other elements, starting with the prior activity
    #REF: https://docs.python.org/3/library/functions.html#range
    for index in range(listLength - 1, -1, -1):
    
        #check if the last compatible activity's start time is >= the current index's end time
        if (tempList[compatibleIndex][1] >= tempList[index][2]):
        
            #store the compatible index
            compatibleList.append(tempList[index][0])
            
            #set variable to store the current compatible index for comparison
            compatibleIndex = index

    #reverse the order of the list for proper display purposes
    #REF: https://www.tutorialspoint.com/python/list_reverse.htm
    compatibleList.reverse()

    return compatibleList

#*******************************************************************************************
# "Main" area for calling the algorithm and displaying the results
#*******************************************************************************************

#variable for display set #
counter = 1

#loop through each list for processing
for list in startFinishList:

    #sort and find the compatible list of indexes
    processedList = lastToStart(list)
    
    #display the appropriate set number by inserting the counter
    #REF: https://stackoverflow.com/questions/12102749/how-can-i-suppress-the-newline-after-a-print-statement
    print('Set {}'.format(counter))
    
    #display the amount of activities via utilizing the list of compatible indices length
    print('Number of activities selected = {}'.format(len(processedList)))
    
    #display "Activities" prior to displaying each number
    print('Activities:', end = ' ')

    #loop through and display each compatible index
    for num in processedList:
        print(num, end = ' ')
    
    #create a line break
    print('\n')
    
    #increment counter
    counter += 1
