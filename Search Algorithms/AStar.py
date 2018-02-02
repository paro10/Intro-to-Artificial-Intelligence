#!/usr/bin/python
''' by Paromita Banerjee

Assignment 3, in CSE 415, Winter 2018.

This file contains my implementation of the
A-Star algorithm.
'''

import sys
import math
from priorityQB import PriorityQB


if sys.argv==[''] or len(sys.argv)<2:
  import EightPuzzle as Problem
  heuristics = lambda s: Problem.HEURISTICS['h_manhattan'](s) #map h_manhattan as heuristic for EightPuzzle
  #import TowersOfHanoi as Problem
else:
  import importlib
  Problem = importlib.import_module(sys.argv[1])
  heuristics = lambda s: Problem.HEURISTICS[sys.argv[2]](s) #map heuristic value entered in command line to dict in EightPuzzleWithHeuristics
  #a=sys.argv[3]
  #initial_state = Problem.CREATE_INITIAL_STATE(a)



print("\nWelcome to A*")
COUNT = None
BACKLINKS = {}
G={} #dict to hold exact cost of the path from the starting point to any vertex n
F={} #cost (distance) of a shortest path
H={} #dict to hold heuristic estimated cost from vertex n to the goal

def runAStar():
  initial_state = Problem.CREATE_INITIAL_STATE() #Initial state creation
  print("Initial State:")
  print(initial_state)
  global COUNT, BACKLINKS, MAX_OPEN_LENGTH, OPEN
  COUNT = 0
  BACKLINKS = {}
  MAX_OPEN_LENGTH = 0
  AStar(initial_state)
  print(str(COUNT)+" states expanded.")
  print('MAX_OPEN_LENGTH = '+str(MAX_OPEN_LENGTH))



def AStar(initial_state):
  global COUNT, BACKLINKS, MAX_OPEN_LENGTH, OPEN
  CLOSED = []
  OPEN=PriorityQB()
  BACKLINKS[initial_state] = None
  G[initial_state] = 0
  H[initial_state] = heuristics(initial_state) #calls heuristic function
  F[initial_state] = H[initial_state]
  #print(initial_state)
  #OPEN.insert(initial_state, 0)
  OPEN.insert(initial_state, F[initial_state]) #insert initial state into OPEN

  while OPEN != []:

    S, F[S] = OPEN.deletemin() #pop from open
    while S in CLOSED: #if state already in closed, pop next value from open
      S = OPEN.deletemin()

    if Problem.GOAL_TEST(S):
      print(Problem.GOAL_MESSAGE_FUNCTION(S))
      path = backtrace(S)
      print('Length of solution path found: '+str(len(path)-1)+' edges')
      return
    COUNT += 1
    CLOSED.append(S)


    L = []
    for op in Problem.OPERATORS:
      if op.precond(S):
        new_state = op.state_transf(S)
        if (new_state in CLOSED):continue #ignore child node
        if (new_state in OPEN): #if already present in open
          new_g = G[S] + 1 #G-score of current node
          if G[new_state] > new_g:
            G[new_state] = new_g #update G-score if new score is better
            BACKLINKS[new_state] =S #update successor links
        else: #If it isn't in the open set, calculate the G and H score for the node
          G[new_state] =G[S] + 1 #G-score of current node assigned to child
          H[new_state]= heuristics(new_state) #find heuristic value of new state
          F[new_state] = G[new_state] + H[new_state] #compute cost
          BACKLINKS[new_state]=S #update successor links
          OPEN.insert(new_state, F[new_state]) #insert new child node into OPEN



def print_state_list(name, lst):
  print(name+" is now: ",end='')
  for s in lst[:-1]:
    print(str(s),end=', ')
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
  runAStar()