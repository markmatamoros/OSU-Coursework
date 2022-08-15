#************************************************
# Program Name: insertsort.py
# Author: Mark Matamoros
# Date: January 15, 2017
# Description: Homework Week 1 - insert sort example
#*************************************************

#****************************************************************
# list creation area for pulling values from text into a list,
# which are stored within another list
#*****************************************************************

#create empty list for integer-list storage
listList = []

#open file for reading
with open("data.txt", 'r') as fileObject:
    
    #iterate through lines in file
    for line in fileObject:
        
        #create a list of numbers that were previously sepearated by whitespace
        tempList = line.split()
        
        #convert the number(strings) into integer values
        tempList = [int(number) for number in tempList]
        
        #add list to the "list of lists"
        listList.append(tempList)

#print(listList)

#*************************************************************************
# insertSort: applies an insertion sort algorithm to a list
# parameters: a list
# Def ref: https://anh.cs.luc.edu/python/hands-on/3.1/handsonHtml/functions.html
# Algorithm ref: http://projectpython.net/chapter13/ and lecture
#*************************************************************************
def insertSort(aList):

    #loop through list, starting with the second element, ending with the last element
    #https://www.pythoncentral.io/pythons-range-function-explained/
    for index in range(1, len(aList)):
        
        #grab index value for comparison
        number = aList[index]

        #grab location prior to index
        prevIndex = index - 1

        #loop compares neighboring values within list via shifting from pair to pair
        #exits when either the pair's left location passes the first list element or the right value...
        #...is larger than the left value.
        while prevIndex >= 0 and aList[prevIndex] > number:
            #temporarily store the pair's right neighbor
            tempValue = aList[prevIndex + 1]
            
            #set neighboring right-location with the left location's value
            aList[prevIndex + 1] = aList[prevIndex]

            #set neighboring left-location with the prior right location's value
            aList[prevIndex] = tempValue
            
            #decrement index for pair comparison and loop handling
            prevIndex -= 1


#**********************
# "main" area
#**********************
file = open("insert.out", 'w')

#loop handles the insertion sort algorithm for each list within the list
for list in listList:
    
    #call the insertion sort algorithm for the list
    insertSort(list)
    
    #loop writes each number in the list
    for number in list:
        #write number
        file.write(str(number))
        
        #write a space between each number
        file.write(" ")
    
    #write a new line for the next list printing
    file.write("\n")
