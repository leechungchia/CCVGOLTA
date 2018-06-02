import node
import numpy as np
import csv
import pandas
from enum import IntEnum
import itertools
import BT
import time

class Action(IntEnum):
    ADVANCE    = 1
    U_TURN     = 2
    TURN_RIGHT = 3
    TURN_LEFT  = 4
    HALT       = 5

class Maze:
    def __init__(self, filepath):
        self.raw_data = pandas.read_csv(filepath).values
        print(self.raw_data)
        self.nodes = []
        self.nd_dict = dict() # key: index, value: the correspond node
        self.explored = set()
        self.startpoint = 0
        self.endpoints = {}
        self.record = {}
        self.Successorstable = {}
        self.bestway = []
        self.way = []
        self.rfid = []
        for dt in self.raw_data:
            dot = [node.Node(int(dt[0]))]
            self.nodes += dot
            self.nd_dict[dot[0].index] = dot[0]
            continue
            #TODO: Update the nodes with the information from raw_data

        for i in range(len(self.nodes)):
            for j in range(1,5):
                suces_index = self.raw_data[self.nodes[i].index-1][j]
                if not np.isnan(suces_index):
                    suces = self.nodes[int(self.raw_data[self.nodes[i].index-1][j])-1]
                    if j == 1:
                        direction = node.Direction.NORTH
                    elif j == 2:
                        direction = node.Direction.SOUTH
                    elif j == 3:
                        direction = node.Direction.WEST
                    elif j == 4:
                        direction = node.Direction.EAST
                    length = self.raw_data[i][j+4]
                    if np.isnan(length):
                        length = 1
                    self.nodes[i].setSuccessor(suces,direction,length)
        for i in self.nodes:
            if len(i.Successors) <= 1:
                self.endpoints[i.index] = i
        for i in self.nodes:
            record  = {}
            for w in self.nodes:
                subnodes = list(map(lambda x :x[0],i.Successors))
                distance = list(map(lambda x :x[2],i.Successors))
                if w in subnodes:
                    record[w] = distance[subnodes.index(w)]
            self.record[i] = record
            continue
                #TODO: Update the successors for each node
        for i in self.nodes:
            self.Successorstable[i] = set(map(lambda x :x[0],i.Successors))

    def getStartPoint(self,index):
        for i in self.nodes:
            if len(i.Successors) <= 1:
                self.endpoints[i.index] = i
        if (len(self.nd_dict) < 2):
            print ("Error: the start point is not included.")
            return 0;
        if index in self.endpoints.keys():
            del self.endpoints[index]
        self.startpoint = self.nd_dict[index]
        return self.nd_dict[index]
    def getways(self,current):
        unvisited = {node: None for node in self.nodes}
        visited = {}
        currentDistance = 0
        unvisited[current] = currentDistance#B到B的距离记为0
        while True:
            for neighbour, distance in self.record[current].items():
                if neighbour not in unvisited:
                    continue
                newDistance = currentDistance + distance#新的距离
                if unvisited[neighbour] is None or unvisited[neighbour] > newDistance:
                    unvisited[neighbour] = newDistance
            visited[current] = currentDistance#这个点已经松弛过，记录
            del unvisited[current]#从未访问过的字典中将这个点删除
            if not unvisited: break#如果所有点都松弛过，跳出此次循环
            candidates = [node for node in unvisited.items() if node[1]]#找出目前还有拿些点未松弛过
            current, currentDistance = sorted(candidates, key = lambda x: x[1])[0]#找出目前可以用来松弛的点
        return visited
    def getway(self,graph,start,goal,path = None):
        if path is None:
            path = [start]
        if start == goal:
            yield path
        for next in graph[start] - set(path):
            yield from self.getway(graph, next, goal, path + [next])
    def getlength(self,start,goal):
        record = []
        collection = list(self.getway(self.Successorstable,start,goal))
        for i in range(len(collection)):
            count = 0
            for w in range(len(collection[i])-1):
                distance = [x for x in collection[i][w].Successors if x[0] == collection[i][w+1] ][0][2]
                count += distance
            record.append(count)
        shortest_distance = min(record)
        route_index = [record.index(x) for x in record if x == shortest_distance]
        route = [x for x in collection if collection.index(x) in route_index]
        return shortest_distance,route
    def data_collect_endpoints(self):
        end_dict = {}
        end = list(self.endpoints.keys())
        a = list(itertools.combinations(end,2))
        for i in a:
            unit = self.getlength(self.endpoints[i[0]],self.endpoints[i[1]])[0]
            register = tuple(sorted([x for x in i]))
            end_dict[register] = unit
        return end_dict

    def BFS(self, nd):
        end_dict = self.data_collect_endpoints()
        record = []
        ndList = []
        length = len(self.endpoints)
        endpoints_index = list(self.endpoints.keys())
        arrange = list(itertools.permutations(endpoints_index))
        collection_distances = {}
        for i in endpoints_index:
            collection_distances[i] = self.getlength(nd,self.nd_dict[i])[0]
        for x in arrange:
            start_distance = collection_distances[x[0]]
            for i in range(length-1):
                distance = end_dict[tuple(sorted([x[i],x[i+1]]))]
                start_distance += distance
            record.append(start_distance)
        shortest_distance = min(record)
        i = record.index(shortest_distance)
        ndList.append(arrange[i])
        """
        for i in range(len(record)):
            if record[i] == shortest_distance:
                ndList.append(arrange[i])
        """
        self.bestway = ndList

        #TODO: design your data structure here for your algorithm
        while (True):
            #TODO: Apply your algorithm here. Make sure your algorithm can update values and stop under some conditions.
            break
        #TODO: update the information of your data structure
        return ndList
    def BFS_2(self, nd):
        register = list(self.endpoints.keys())
        ndlist = []
        """ return a sequence of nodes of the shortest path"""
        #TODO: similar to BFS but fixed start point and end point
        while len(register) > 0:
            shortest = self.getlength(nd,self.nd_dict[register[0]])[0]
            record = register[0]
            for i in register[1:]:
                distance = self.getlength(nd,self.nd_dict[i])[0]
                if distance < shortest:
                    record = i
                    shortest = distance
            ndlist.append(record)
            del register[register.index(record)]
        self.bestway = [ndlist]
        return ndlist

    def getAction(self, car_dir, nd_from, nd_to):
        """ return an action and the next direction of the car """
        if nd_from.isSuccessor(nd_to):
            nd_dir = nd_from.getDirection(nd_to)
            #TODO: Return the action based on the current car direction and the direction to next node
            print("Error: Failed to get the action")
            return 0
        else:
            print("Error: Node(",nd_to.getIndex(),") is not the Successor of Node(",nd_from.getIndex(),")")
            return 0

    def strategy(self):
        first_strategy = [self.startpoint.index] + list(self.bestway[0])
        first_place = first_strategy[0]
        record = [first_place]
        record_2 = []
        for i in range(len(first_strategy)-1):
            road = self.illusion(min(self.getlength(self.nd_dict[first_strategy[i]],self.nd_dict[first_strategy[i+1]])[1]))
            record += road[1:len(road)]
        for i in range(len(record)-1):
            record_2 += [x[1] for x in self.nd_dict[record[i]].Successors if x[0] == self.nd_dict[record[i+1]]]
        case = len(record_2)
        condition = 2
        way = []
        for i in range(len(record_2)):
            if record_2[i] == condition:
                way += ["goforward"]
            elif record_2[i] == 3 and condition == 2:
                way += ["turnright"]
            elif record_2[i] == 3 and condition == 1:
                way += ["turnleft"]
            elif record_2[i] == 4 and condition == 1:
                way += ["turnright"]
            elif record_2[i] == 4 and condition == 2:
                way += ["turnleft"]
            elif record_2[i] == 1 and condition == 3:
                way += ["turnright"]
            elif record_2[i] == 1 and condition == 4:
                way += ["turnleft"]
            elif record_2[i] == 2 and condition == 3:
                way += ["turnleft"]
            elif record_2[i] == 2 and condition == 4:
                way += ["turnright"]
            elif (record_2[i] == 2 and condition == 1) or (record_2[i] == 1 and condition == 2) or (record_2[i] == 3 and condition == 4) or (record_2[i] == 4 and condition == 3):
                way += ["turnaround"]
            condition = record_2[i]
        self.way = way
        return record,record_2,way
    def strategy_process(self):
        condition_dict = {"S":"stop","T":"track","G":"goforward","R":"turnright","L":"turnleft","A":"turnaround"}
        res = dict((v,k) for k,v in condition_dict.items())
        case = -len(self.way)
        rfid = list(map(lambda x:x=="turnaround",self.way))
        messeage = BT.bluetooth()
        print(messeage.do_connect("COM3",9600,timeout = 2))
        messeage.SerialWrite("T")
        a = messeage.SerialReadString()
        while a != "S":
            a = messeage.SerialReadString()
        while case < 0:
            a = messeage.SerialReadString()
            if a == "S" and rfid[case] == False:
                while True:
                    command = self.way[case]
                    messeage.SerialWrite(res[command])
                    #time.sleep(0.1)
                    data = messeage.SerialReadString()
                    if data == res[command]:
                        case += 1
                        break
            elif a == "S" and rfid[case] == True:
                while True:
                    command = self.way[case]
                    messeage.SerialWrite("F")
                    data = messeage.SerialReadByte()
                    self.rfid.append(data)
                    if data == "46":
                        case += 1
                        break
                """
                while True:
                    command = self.way[case]
                    messeage.SerialWrite(res[command])
                    #time.sleep(0.1)
                    data = messeage.SerialReadString()
                    if data == res[command]:
                        break
                """
            """
            elif a == "R" or a == "L" or a == "A" or a == "G":
                while True:
                    messeage.SerialWrite("T")
                    time.sleep(0.1)
                    data = messeage.SerialReadString()
                    if data == "T":
                        break
        """
        n = 1
        while n == 1:
            messeage.SerialWrite("T")
            data = messeage.SerialReadByte()
            if data == "53":
                while True:
                    messeage.SerialWrite("Z")
                    data = messeage.SerialReadByte()
                    self.rfid += [data]
                    if data == "46":
                        n = 0
                        break

    def strategy_2(self, nd_from, nd_to):
        return self.BFS_2(nd_fro, nd_to)
    def illusion(self,ndlist):
        record = []
        for i in ndlist:
            if type(i) == list:
                record.append(self.illusion(i))
            else:
                a = i.index
                record.append(a)
        return record
    def func(self):
        small = node_neighbor_distances + small_neighbour_goal_distance
a = Maze("maze_405_0508.csv")
print(a.endpoints.keys())
a.getStartPoint(1)
#print(a.illusion(list(a.getway(a.Successorstable,a.nd_dict[2],a.nd_dict[1]))))
#print(a.getlength(a.nd_dict[2],a.nd_dict[1]))
start = time.time()
print(a.BFS_2(a.nd_dict[1]))
print(a.strategy()[0])
end = time.time()
print(end-start)
start = time.time()
print(a.BFS(a.nd_dict[1]))
print(a.strategy()[0])
end = time.time()
print(end-start)
#print(a.way)
#a.strategy_process()
#print(a.rfid)

