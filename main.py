from node import *
import maze as mz
import score
import student
import BT
import numpy as np
import pandas
import time
import sys
import os

def main():
    maze = mz.Maze("maze_405_0508.csv")
    next_nd = maze.getStartPoint(1)
    car_dir = Direction.SOUTH
    point = score.Scoreboard("score1.csv")
    #interface = student.interface()         the part of calling student.py was commented out.

    if(sys.argv[1] == '0'):
        maze.strategy_process(point,sys.argv[1])
            #TODO: Impliment your algorithm here and return the UID for evaluation function
            # ================================================
            # Basically, you will get a list of nodes and corresponding UID strings after the end of algorithm.
			# The function add_UID() would convert the UID string score and add it to the total score.
			# In the sample code, we call this function after getting the returned list. 
            # You may place it to other places, just make sure that all the UID strings you get would be converted.
            # ================================================
    elif(sys.argv[1] == '1'):
        ndlist = []
            #TODO: Implement your algorithm here and return the UID for evaluation function
        for i in range(5):
            nd = int(input("destination: "))
            ndlist.append(nd)
        maze.bestway = [ndlist]
        maze.strategy_process(point,sys.argv[1])
        if(len(ndlist) == 0):
            print("end process")
            print('')
        else:
            print("unfinished nodes:" + ','.join([str(x) for x in ndlist]))
    """
    node = 0
    while(not node):
        node = interface.wait_for_node()

    interface.end_process()
    """
    print("complete")
    print("")
    a = point.getCurrentScore()
    print("The total score: ", a)

if __name__=='__main__':
    main()