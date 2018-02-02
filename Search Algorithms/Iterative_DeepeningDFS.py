'''IDDFS.py
by Paromita Banerjee

Assignment 3, in CSE 415, Winter 2018.

This file contains my problem formulation for the problem of
the Iterative Deepening Depth First Search.
'''
import sys

if sys.argv==[''] or len(sys.argv)<2:
#  import EightPuzzle as Problem
  import TowersOfHanoi as Problem
#  import Farmer_Fox_etc as Problem
#  import Find_the_Number as Problem
else:
  import importlib
  Problem = importlib.import_module(sys.argv[1])

print("\nWelcome to ItrDDFS")
COUNT = 0
BACKLINKS = {}
OPEN=[]

def runIDDFS():
  initial_state = Problem.CREATE_INITIAL_STATE()
  print("Initial State:")
  print(initial_state)
  global COUNT, BACKLINKS, MAX_OPEN_LENGTH, L
  OPEN.append(initial_state)
  BACKLINKS[initial_state] = None
  #BACKLINKS = {}
  MAX_OPEN_LENGTH = 0
  for limit in range(1000000000000000000): #Substituting infinity with a large value
    result=IDDFS(initial_state, limit)
    print("DLS Result for depth ",limit," is: ", result)
    if result==True:break #if flag true, break out of loop
  print(str(COUNT)+" states expanded.")
  print('MAX_OPEN_LENGTH = '+str(MAX_OPEN_LENGTH))


def IDDFS(state, max_depth):
    for limit in range(max_depth): #Limit depth of each iteration
        COUNT=0
        if DLS(state, limit) == True:
            return True
    return False


#DEPTH LIMITED SEARCH
def DLS(state, limit):
    global MAX_OPEN_LENGTH, COUNT
    if len(OPEN)>MAX_OPEN_LENGTH: MAX_OPEN_LENGTH = len(OPEN)
    if Problem.GOAL_TEST(state):
        print(Problem.GOAL_MESSAGE_FUNCTION(state))
        path = backtrace(state)
        print('Length of solution path found: '+str(len(path)-1)+' edges')
        return True

    if limit <= 0: #Irrelevant Limit value
        return False;


    for op in Problem.OPERATORS:
        if op.precond(state):
            child=op.state_transf(state)
            if not (child in OPEN): #If child does not exist in OPEN
                OPEN.append(child)
                BACKLINKS[child]=state #Update successor link
                COUNT +=1
                print_state_list("OPEN", OPEN)
            if DLS(child, limit-1): #Recursively call DLS on child node by decreasing limit from max_depth to 0
                return True

    return False




def print_state_list(name, lst):
  print(name+" is now: ",end='')
  for s in lst[:-1]:
    print('\n'+str(s),end=', ')
  print(str(lst[-1]))

def backtrace(S):
  global BACKLINKS
  path = []
  while S:
    path.append(S)
    S = BACKLINKS[S]
  path.reverse()
  print("Solution path: ")
  for s in path:
    print(s)
  return path

def report(open, closed, count):
  print("len(OPEN)="+str(len(open)), end='; ')
  print("len(CLOSED)="+str(len(closed)), end='; ')
  print("COUNT = "+str(count))

if __name__=='__main__':
  runIDDFS()
