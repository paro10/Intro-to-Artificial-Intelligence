'''EightPuzzleWithHeuristics.py
by Paromita Banerjee

Assignment 3, in CSE 415, Winter 2018.

This file contains my problem formulation for the problem of
the EightPuzzleWithHeuristics.
'''

import math
#<METADATA>
QUIET_VERSION = "0.2"
PROBLEM_NAME = "Eight Puzzle"
PROBLEM_VERSION = "0.2"
PROBLEM_AUTHORS = ['P. Banerjee']
PROBLEM_CREATION_DATE = "27-JAN-2018"
PROBLEM_DESC=\
'''This formulation of the Eight Puzzle uses generic
Python 3 constructs and has been tested with Python 3.6.
It is designed to work according to the QUIET2 tools interface.
'''
#</METADATA>

#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>
class State:
  def __init__(self, b):
    if len(b)==9:
      list_of_lists = [b[:3],b[3:6],b[6:]]
    else:
      list_of_lists = b
    self.b = list_of_lists

  def __eq__(self,s2):
    for i in range(3):
      for j in range(3):
        if self.b[i][j] != s2.b[i][j]: return False
    return True

  def __str__(self):
    # Produces a textual description of a state.
    # Might not be needed in normal operation with GUIs.
    txt = "\n["
    for i in range(3):
      txt += str(self.b[i])+"\n "
    return txt[:-2]+"]"

  def __hash__(self):
    return (self.__str__()).__hash__()

  def copy(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State({})
    news.b = [row[:] for row in self.b]
    return news

  def find_void_location(self):
    '''Return the (vi, vj) coordinates of the void.
    vi is the row index of the void, and vj is its column index.'''
    for i in range(3):
      for j in range(3):
        if self.b[i][j]==0:
          return (i,j)
    raise Exception("No void location in state: "+str(self))

  def can_move(self,dir):
    '''Tests whether it's legal to move a tile that is next
       to the void in the direction given.'''
    (vi, vj) = self.find_void_location()
    if dir=='N': return vi<2
    if dir=='S': return vi>0
    if dir=='W': return vj<2
    if dir=='E': return vj>0
    raise Exception("Illegal direction in can_move: "+str(dir))

  def move(self,dir):
    '''Assuming it's legal to make the move, this computes
       the new state resulting from moving a tile in the
       given direction, into the void.'''
    news = self.copy() # start with a deep copy.
    (vi, vj) = self.find_void_location()
    b = news.b
    if dir=='N':
      b[vi][vj] = b[vi+1][vj]
      b[vi+1][vj] = 0
    if dir=='S':
      b[vi][vj] = b[vi-1][vj]
      b[vi-1][vj] = 0
    if dir=='W':
      b[vi][vj] = b[vi][vj+1]
      b[vi][vj+1] = 0
    if dir=='E':
      b[vi][vj] = b[vi][vj-1]
      b[vi][vj-1] = 0
    return news # return new state



class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)



#</COMMON_CODE>

#<INITIAL_STATE>
  # Use default, but override if new value supplied
             # by the user on the command line.
try:
  import sys
  import importlib
  #Puzzle = importlib.import_module(sys.argv[3])
  init_state_string = sys.argv[3]
  print("Initial state as given on the command line: "+init_state_string)
  #init_state_list =globals().get(Puzzle,CREATE_INITIAL_STATE)
  #init_state_list = Puzzle.CREATE_INITIAL_STATE()
  #init_state_list=exec(init_state_string)
  #init_state_list = lambda s: Puzzle.CREATE_INITIAL_STATE()
  #print(init_state_list)

  #init_state_list =exec(init_state_string, globals())
  #init_state_list = getattr(Puzzle, init_state_string)()
  init_state_list = eval(init_state_string)
except:
  #init_state_list = [[8, 7, 6], [5, 4, 3], [2, 1, 0]]
  print("Using default initial state list: "+str(init_state_list))
  print(" (To use a specific initial state, enter it on the command line, e.g.,")
  print("python3 ../Int_Solv_Client.py EightPuzzle '[[3, 1, 2], [0, 4, 5], [6, 7, 8]]'")

CREATE_INITIAL_STATE = lambda: State(init_state_list)
#</INITIAL_STATE>

#<OPERATORS>
directions = ['N','E','W','S']
OPERATORS = [Operator("Move a tile "+str(dir)+" into the void",
                      lambda s,dir1=dir: s.can_move(dir1),
                      # The default value construct is needed
                      # here to capture the value of dir
                      # in each iteration of the list comp. iteration.
                      lambda s,dir1=dir: s.move(dir1) )
             for dir in directions]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

def h_euclidean(state): #Function to compute euclidean distance
    s=state.b #accessing state object
    s=[item for sublist in s for item in sublist] #flatteing nested list into a list
    #print("S",s)
    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8] #the goal state
    #print("GOAL",goal)
    result = 0

    for i in s:
      index = s.index(i) #index of i-th element in current state
      g_index = goal.index(i) #index of same element in goal state
      c_row = index // 3 #current row
      c_col = index % 3 #current column
      g_row = g_index // 3 #goal row
      g_col = g_index % 3 #goal column
      result += math.sqrt(pow(g_row - c_row, 2) + pow(g_col - c_col, 2))
    return result


def h_hamming(state):
  s=state.b
  s=[item for sublist in s for item in sublist] #flatteing nested list into a list
  goal = [0, 1, 2, 3, 4, 5, 6, 7, 8] #the goal state
  count=0
  for i in s:
    index = s.index(i) #index of i-th element in current state
    g_index = goal.index(i) #index of same element in goal state
    if index!=g_index:
      count+=1 #no. of tiles that are out of place
  return count

def h_manhattan(state):
  s=state.b
  s=[item for sublist in s for item in sublist] #flatteing nested list into a list
  goal = [0, 1, 2, 3, 4, 5, 6, 7, 8] #the goal state
  distance=0
  for i in s:
    index=s.index(i) #index of i-th element in current state
    g_index=goal.index(i)  #index of same element in goal state
    c_row = index // 3
    c_col = index % 3
    g_row = g_index // 3
    g_col = g_index % 3
    total_diff=abs(g_row-c_row) + abs(g_col-c_col)
    distance+=total_diff
  return distance

def h_custom(state):
  s=state.b
  s=[item for sublist in s for item in sublist] #flatteing nested list into a list
  goal = [0, 1, 2, 3, 4, 5, 6, 7, 8] #the goal state
  D=1
  D2=math.sqrt(2)
  distance=0
  for i in s:
    index=s.index(i) #index of i-th element in current state
    g_index=goal.index(i)  #index of same element in goal state
    c_row = index // 3
    c_col = index % 3
    g_row = g_index // 3
    g_col = g_index % 3
    dx=abs(c_row-g_row) #absolute distance between current row and goal row
    dy=abs(c_col-g_col) #absolute distance between current column and goal column
    distance+=D*(dx+dy)+(D2-2*D)*min(dx,dy) #Octile Distance, by relaxing the constraint that we could move the pieces diagonally.
  return distance


def goal_test(s):
  '''If all the b values are in order, then s is a goal state.'''
  return s == State([[0,1,2],[3,4,5],[6,7,8]])

def goal_message(s):
  return "You've got all eight straight. Great!"

HEURISTICS = {'h_euclidean': h_euclidean, 'h_hamming': h_hamming, 'h_manhattan': h_manhattan, 'h_custom': h_custom} #Dict of heuristics for mapping