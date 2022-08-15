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

#*************************************************************************
# stoogeSort: applies a stooge sort algorithm to a list
# parameters: a list
# Def ref: https://anh.cs.luc.edu/python/hands-on/3.1/handsonHtml/functions.html
# Algorithm ref: Homework Pseudocode
#*************************************************************************
import random
import time

def stoogeSort(aList, start, end):

    #calculate array length
    arrayLength = end - start + 1

    #handle base case when array length equals 2, thereafter
    #compare first to second value and swap if necessary
    if (arrayLength == 2 and aList[start] > aList[end]):
        #temporarily hold first number
        tempNum = aList[start]
        
        #swap second value to first location
        aList[start] = aList[end]
        
        #insert first value into second element location
        aList[end] = tempNum

    #handles the recursion component, where the length is greater than two
    elif (arrayLength > 2):
        #calculate a third of the array, as opposed to the two/thirds location
        #found it easier to handle
        m = arrayLength // 3

        #process the beginning to the end of the second third
        stoogeSort(aList, start, end - m)
        
        #process the beginning of the first third to the end
        stoogeSort(aList, start + m, end)
        
        #process the beginning to the end of the second third
        stoogeSort(aList, start, end - m)


#**********************
# "main" area
#**********************

#create a variable to hold amount of random values to be inserted into a list
n = 900

#create an empty list
list = []

#create a list of randomly generated values
for i in range (n):
    #append randomly generated numbers into a list
    #numbers are start at 1, end at 101, and have a step of 1 (integer values)
    #generates values from 1 to 100
    #ref:https://docs.python.org/2/library/random.html
    list.append(random.randrange(1, 101, 1))

#grab start time for the algorithm
#Ref: https://docs.python.org/2/library/timeit.html
startTime = time.time()

#sort list with the stooge sort algorithm
stoogeSort(list, 0, len(list)-1)

#grab the end time for the algorithm
stopTime = time.time()

#print the resulting time
print (stopTime - startTime)

