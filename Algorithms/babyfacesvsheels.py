#******************************************************************************
# Program Name: babyfacesvsheels.py
# Author: Mark Matamoros
# Date: February 18, 2018
# Description: Homework Week 6 - Babyfaces vs Heels (BHS)
#******************************************************************************
import sys                              #for command line argument
from collections import defaultdict     #for dictionary
from collections import deque           #for deque

file = sys.argv[1]  #store command line's argument file

wrestlerList = []   #list for wrestlers
pairList = []       #list of rival wrestler pairs

#dictionary holds rival (wrestler) edges, stemming from the key (wrestler)
#REF:https://docs.python.org/2/library/collections.html
rivalEdges = defaultdict(list)

#dictionary holds wrestler's (key) team
wrestlerTeamAssoc = defaultdict(list)

#deque for BFS
wrestlerDeque = deque()

#***********************************************************************************
# Area handles list and dictionary insertion for BHS prepping
# Creates lists for wrestlers and wrestler match pairs
# Creates dictionaries for wrestler's team affiliation and wrestler edges
#***********************************************************************************

#flag for handling appropriate list insertion (wrestler and pair insertions)
flag = -1

#open file for reading
with open(file, 'r') as fileObject:
 
    #iterate through lines in file
    for line in fileObject:
        
        #exit loop if the next line is a line break
        #this is based on the file's formatting
        if (line == '\n'):
            break
        
        #strip the line's line break
        line = line.strip('\n')

        #for skipping integer line and prepping wrestler and pair list insertion
        #check if the line is a digit
        if (line.isdigit()):

            #raise intialized flag to 0 (preps for wrestler insertion)
            flag += 1

        #handles wrestler and pair insertion
        else:
            #for inserting wrestlers into a list
            if (flag == 0):
                #append wrestler into wrestler list
                wrestlerList.append(line)
            else:
                #convert rival pair into a list format
                tempList = line.split()

                #append rival pairing into pair list
                pairList.append(tempList)

#loop through wrestler pair list for edge dictionary insertion
#keys are the wrestlers
#REF:https://docs.python.org/2/library/collections.html
for rival in pairList:
    #store "right-side" rival to wrestler key's list
    rivalEdges[rival[0]].append(rival[1])
    
    #store "left-side" rival to wrestler key's list
    rivalEdges[rival[1]].append(rival[0])

#loop through wrestler list for wrestler team dictionary insertion
for wrestler in wrestlerList:
    #initialize dictionary keys (wrestlers) to "none" (no current affiliation)
    wrestlerTeamAssoc[wrestler].append("none")

#********************************************************************************
# Area handles BFS for a wrestler graph.  This is a modified version:
# 1. Set to handle forest graphs.
# 2. Any new tree has it's first node (wrestler) automatically assigned to the
#    babyface team.
# 3. Each discovered node (wrestler) is assigned to the opposite parent
#    node's (wrestler's) team.
# 4. Complete's when every node (wrestler) has an assigned team.
#********************************************************************************

#loop through each wrestler for BHS (for handling forests)
for i in range(0, len(wrestlerList)):
    
    #implement BHS process for wrestler's without a team (tree in forest)
    if (wrestlerTeamAssoc[wrestlerList[i]] == ["none"]):
    
        #place wrestler within the deque
        wrestlerDeque.append(wrestlerList[i])
        
        #set babyface team to the wrestler key
        wrestlerTeamAssoc[wrestlerList[i]] = ["babyface"]

        #loop through deque until empty
        while wrestlerDeque:
            #pop deque for wrestler node processing
            u = wrestlerDeque.popleft()

            #loop through edges (other wrestlers) connected to wrestler
            for v in rivalEdges[u]:
                #if discovered wrestler does not have a team, give a team
                if (wrestlerTeamAssoc[v] == ["none"]):
                    #for parent wrestler on babyface team
                    if (wrestlerTeamAssoc[u] == ["babyface"]):
                        #other wrestler will be on the heel team
                        wrestlerTeamAssoc[v] = ["heel"]
                    #for parent wrestler on the heel team
                    else:
                        #other wrestler will be on the babyface team
                        wrestlerTeamAssoc[v] = ["babyface"]
                    #add other wrestler to the deque
                    wrestlerDeque.append(v)

#*******************************************************************************
# Area compares wrestler pairs to determine proper set of rivalries.
# Notifies user if it is possible or impossible.  If possible, the program
# will display each team's members.
#*******************************************************************************

possible = "Yes"        #for displaying possible or impossible pairings

#check if wrestling pairs are invalid via looping through wrestler pair list
for pairs in pairList:
    #compare paired wrestlers' teams for same team
    if (wrestlerTeamAssoc[pairs[0]] == wrestlerTeamAssoc[pairs[1]]):
        #set variable for impossible pairing
        possible = "No"
        break

#if variable is set to impossible, notify user
if (possible == "No"):
    print(possible)

#pairings are possible; notify user and display each team's names
else:
    print(possible)
    print("Babyfaces: ", end = "")

    #loop through wrestler team dictionary to locate and print babyface names
    for i in wrestlerTeamAssoc:
        #check if wrestler is a babyface
        if (wrestlerTeamAssoc[i] == ["babyface"]):
            #print babyface name
            print(i, end = " ")

    print("")

    print("Heels: ", end = "")

    #loop through wrestler team dictionary to locate and print heel names
    for i in wrestlerTeamAssoc:
        #check if wrestler is a heel
        if (wrestlerTeamAssoc[i] == ["heel"]):
            #print heel name
            print(i, end = " ")

    print("")

#*************************************
#List and Dictionary troubleshooting
#*************************************
#print(wrestlerList)
#print(pairList)
#print(rivalEdges)
#print(wrestlerTeamAssoc)
