#*******************************************************
# Program Name: makingchange.py
# Author: Mark Matamoros
# Date: January 29, 2018
# Description: Homework Week 3 - making change example
#*******************************************************

#****************************************************************
# list creation area for pulling values from text into a list,
# which are stored within another list
#****************************************************************

#create empty list for integer-list storage
listList = []

#open file for reading
with open("amount.txt", 'r') as fileObject:
    
    #iterate through lines in file
    for line in fileObject:
        
        #create a list of numbers that were previously sepearated by whitespace
        tempList = line.split()
        
        #convert the number(strings) into integer values
        tempList = [int(number) for number in tempList]
        
        #add list to the "list of lists"
        listList.append(tempList)

#************************************************************************************
# makingChange: creates an optimal coin count for inputed integers, based
# on a list of coin denominations.  Furthermore, the individual coin counts
# are also calculated
# parameters: list containing coin denomination values (int's), change amount (int)
#*************************************************************************************
def makingChange(coinDenoms, changeAmount):
    
    #holds optimal minimum # of coins to make the change amount of current change value
    optimalMinCoins = [0]
    
    #indexes hold last coin used to make the respective change amount
    lastUsedCoins = [0]

    #holds coin counts for the individual denominations utilized for the optimized coin amount
    usedDenomCounts = [0] * len(coinDenoms)

    #calculate all change amounts (starting with 1) to the final change amount
    for curChangeAmount in range(1, changeAmount + 1):
        
        #initialize values
        coinCount = curChangeAmount     #stores optimized coin count during evaluation 
        lastCoinUsed = 1                #the last coin used will be at least a penny
                
        #cycle through each coin denomination value
        for aCoinDenom in coinDenoms:
            
            #check if coin denomination is <= the current change amount
            if (aCoinDenom <= curChangeAmount):
        
                #check if a prior optimized index value +1 is less than the current coin count
                if ((1 + optimalMinCoins[curChangeAmount - aCoinDenom]) < coinCount):
                    
                    #grab the prior optimized index's value and increment it
                    #Thereafter, store the result
                    coinCount = 1 + optimalMinCoins[curChangeAmount - aCoinDenom]
            
                    #store the last utilized coin denomination
                    lastCoinUsed = aCoinDenom

        #add the optimal coin amount to the respective list
        optimalMinCoins.append(coinCount)

        #add the last used coin denomination to the respective list
        lastUsedCoins.append(lastCoinUsed)

    #grab the originally inputted change amount
    totalChange = changeAmount
    
    #loop handles the incrementing of denomination values utilized within...
    #...the optimized coin amount
    while totalChange > 0:
    
        #store the index's (used coin) denomination value
        usedCoin = lastUsedCoins[totalChange]
    
        #find the index location of the used coin within the coin denomination array
        #REF:https://www.tutorialspoint.com/python/list_index.htm
        #increment the denomination count
        usedDenomCounts[coinDenoms.index(usedCoin)] += 1
    
        #set variable to find the prior index's used coin value
        totalChange -= usedCoin
    
    #send the list of denomination counts and the optimized coin count
    return usedDenomCounts, optimalMinCoins[changeAmount]


#**********************
# "main" area
#**********************

#create file
file = open("change.txt", 'w')

count = 0           #holds a loop iteration count for calling the makingChange function
denomList = 0       #holds the list index for a denomination list
changeList = 1       #holds the list index for the respective coin amount

#loop handles the dp making change algorithm for each denomination list
#and its associative change amount
for list in listList:
    
    #write the denomination list and its associative change amount
    for number in list:
        #write number
        file.write(str(number))

        #write a space between each number
        file.write(" ")

    #write a new line
    file.write("\n")

    #for every two printed lists from the inputted text, utilize the making change function
    if (count % 2 == 1):
        
        #call the making change algorithm and store its results in a list
        tempList = makingChange(listList[denomList], listList[changeList][0])

        #write the calculated coin denomination count
        for num in tempList[0]:

                #write number
                file.write(str(num))
        
                #write a space between each number
                file.write(" ")

        #write a new line
        file.write("\n")

        #write the optimized coin amount
        file.write(str(tempList[1]))

        #write a new line
        file.write("\n")

        #set the index for the next two lists
        denomList += 2
        changeList += 2

    count += 1  #increment the loop counter
