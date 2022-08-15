#************************************************
# Program Name: mergesort.py
# Author: Mark Matamoros
# Date: January 15, 2017
# Description: Homework Week 1 - merge sort example
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
# mergeSort: applies a merge sort algorithm to a list
# parameters: a list
# Def ref: https://anh.cs.luc.edu/python/hands-on/3.1/handsonHtml/functions.html
# Algorithm ref: http://projectpython.net/chapter13/ and lecture
#*************************************************************************
def mergeSort(aList):
    
    #loop if list contains more than one element
    if len(aList) <= 1:

        #perform floor division to determine the middle element location of the list
        #https://stackoverflow.com/questions/19507808/python3-integer-division
        middle = len(aList) // 2

        #create sublist (left) via ":" delimiter insertion - beginning to middle element location
        #https://docs.python.org/2/tutorial/introduction.html
        leftList = aList[:middle]
        
        #create sublist (right) via ":" delimiter insertion - middle element location to end
        #https://docs.python.org/2/tutorial/introduction.html
        rightList = aList[middle:]

        #recursive call to handle left and right sided lists
        mergeSort(leftList)
        mergeSort(rightList)

        #unwinding...
        
        #initialize all list pointers before the merging process
        leftPointer = 0
        rightPointer = 0
        mergePointer = 0

        #begin merging...
        
        #loop for merge insertion via comparisons of sublists that both contain unused elements
        while i < len(leftList) and j < len(rightList):
            
            #compare the left list's pointed-element to the right list's pointed-element
            #handles the case of a smaller left element
            if leftList[leftPointer] < rightList[rightPointer]:
                
                #add the smaller left list element to the merged list
                aList[mergePointer] = leftList[leftPointer]
                
                #increment pointer for the left list
                leftPointer = leftPointer + 1
            
            #handles the case of a larger or equal element on the left
            else:
                #add the smaller right list element to the merged list
                aList[mergePointer] = rightList[rightPointer]
                
                #increment pointer for the right list
                rightPointer = rightPointer + 1
            
            #increment pointer for the merged list
            mergePointer = mergePointer + 1

        #beginning of case handling where one of the sublists does not have an available element

        #loop for full merge insertion from left sublist, if right sublist does not have available elements
        while leftPointer < len(leftList):
            #add the element to the merged list
            aList[k] = leftList[i]
            
            #increment pointer for the left list
            leftPointer = leftPointer + 1
            
            #increment pointer for the merged list
            mergePointer = mergePointer + 1
        
        #loop for full merge insertion from right sublist, if left sublist does not have available elements
        while rightPointer < len(rightList):
            #add the element to the merged list
            aList[k] = rightList[j]
            
            #increment pointer for the right list
            rightPointer = rightPointer + 1
            
            #increment pointer for the merged list
            mergePointer = mergePointer + 1


#**********************
# "main" area
#**********************
file = open("merge.out", 'w')

#loop handles the merge sort algorithm for each list within the list
for list in listList:
    
    #call the merge sort algorithm for the list
    mergeSort(list)
    
    #loop writes each number in the list
    for number in list:
        #write number
        file.write(str(number))
        
        #write a space between each number
        file.write(" ")
    
    #write a new line for the next list printing
    file.write("\n")
