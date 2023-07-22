# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Shang-Tse Chen (stchen@csie.ntu.edu.tw) on 03/03/2022
from maze import Maze
#import numpy as np
from math import sqrt
import heapq
"""
This is the main entry point for HW1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,fast)

def search(maze: Maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "fast": fast,
    }.get(searchMethod)(maze)

def bfs(maze: Maze): #no problem.....probably
    start: tuple=maze.getStart()
    fringe: list=[] #queue
    path=[start]
    visited_nodes=[]
    fringe.insert(0,((start,[]),path))
    while len(fringe)!=0:
        current,currentpath=fringe.pop()
        if current not in visited_nodes:
            visited_nodes=visited_nodes+[current]
        #print(currentpath)
            if current[0] not in current[1] and current[0] in maze.getObjectives():
                current[1].append(current[0])
                #visited_nodes=[]
                #print(current[1])
                if set(current[1]) == set(maze.getObjectives()):
                    return currentpath
            for i in maze.getNeighbors(current[0][0],current[0][1]):
                if (i,current[1].copy()) not in visited_nodes:
                    fringe.insert(0,((i,current[1].copy()),currentpath+[i]))
        #print(currentpath)


def astar(maze: Maze):
    start: tuple=maze.getStart()
    fringe: list=[] #queue
    path=[start]
    visited_nodes=dict()
    fringe.insert(0,(heuristic(start,maze.getObjectives(),len(maze.getObjectives())),(start,maze.getObjectives()),path,0))
    while len(fringe)!=0:
        _,current,currentpath,cost=heapq.heappop(fringe)#current --> current node and remain goals
        if visited_nodes.get((current[0],tuple(current[1])))==None:
            visited_nodes[(current[0],tuple(current[1]))]=1
           # print(currentpath)
            if current[0] in current[1]:#current[0]-->node coordinates
                current[1].remove(current[0])
                if len(current[1])==0:
                    return currentpath
            for i in maze.getNeighbors(current[0][0],current[0][1]):
                if visited_nodes.get((i,tuple(current[1])))==None:
                    heapq.heappush(fringe, (heuristic(i,current[1].copy(),len(current[1]))+cost, (i,current[1].copy()), currentpath+[i],cost+1))


def astar_corner(maze):
    start: tuple=maze.getStart()
    fringe: list=[] #queue
    path=[start]
    visited_nodes=dict()
    fringe.insert(0,(heuristic(start,maze.getObjectives(),len(maze.getObjectives())),(start,maze.getObjectives()),path,0))
    while len(fringe)!=0:
        _,current,currentpath,cost=heapq.heappop(fringe)#current --> current node and remain goals
        if visited_nodes.get((current[0],tuple(current[1])))==None:
            visited_nodes[(current[0],tuple(current[1]))]=1
           # print(currentpath)
            if current[0] in current[1]:#current[0]-->node coordinates
                current[1].remove(current[0])
                if len(current[1])==0:
                    return currentpath
            for i in maze.getNeighbors(current[0][0],current[0][1]):
                if visited_nodes.get((i,tuple(current[1])))==None:
                    heapq.heappush(fringe, (heuristic(i,current[1].copy(),len(current[1]))+cost, (i,current[1].copy()), currentpath+[i],cost+1))

def realdistance(maze: Maze,start,final): #no problem.....probably
    fringe: list=[] #queue
    visited_nodes=dict()
    fringe.insert(0,(start,0))
    while len(fringe)!=0:
        current,currentpathlen=fringe.pop()
        if visited_nodes.get((current[0],current[1]))==None:
            visited_nodes[current[0],current[1]]=1
        #print(currentpath)
            if current == final:
                return currentpathlen
            for i in maze.getNeighbors(current[0],current[1]):
                if visited_nodes.get((i[0],i[1]))==None:
                    fringe.insert(0,(i,currentpathlen+1))
    
def heuristic(node,dots,len):
    a=0
    min=999999999
    for dot in dots:
        a=abs(node[0]-dot[0])+abs(node[1]-dot[1])
        if a<min:
            min=a
    return min+len
    
    
def heuristic1(node,dots,len):#len -->numbers of remain goals
    a=0
    min=99999999999
    for dot in dots:
        a=abs(node[0]-dot[0])+abs(node[1]-dot[1])
        if a<min:
            min=a
    return min+100*len
def astar_multi(maze: Maze):
    start: tuple=maze.getStart()
    fringe: list=[] #queue
    path=[start]
    visited_nodes=dict()
    fringe.insert(0,(heuristic(start,maze.getObjectives(),len(maze.getObjectives())),(start,maze.getObjectives()),path,0))
    while len(fringe)!=0:
        _,current,currentpath,cost=heapq.heappop(fringe)#current --> current node and remain goals
        if visited_nodes.get((current[0],tuple(current[1])))==None:
            visited_nodes[(current[0],tuple(current[1]))]=1
           # print(currentpath)
            if current[0] in current[1]:#current[0]-->node coordinates
                current[1].remove(current[0])
                if len(current[1])==0:
                    return currentpath
            for i in maze.getNeighbors(current[0][0],current[0][1]):
                if visited_nodes.get((i,tuple(current[1])))==None:
                    heapq.heappush(fringe, (heuristic(i,current[1].copy(),len(current[1]))+cost, (i,current[1].copy()), currentpath+[i],cost+1))
    
def fast(maze: Maze):
    start: tuple=maze.getStart()
    fringe: list=[] #queue
    path=[start]
    visited_nodes=dict()
    fringe.insert(0,(heuristic1(start,maze.getObjectives(),len(maze.getObjectives())),(start,maze.getObjectives()),path,0))
    while len(fringe)!=0:
        _,current,currentpath,cost=heapq.heappop(fringe)#current --> current node and remain goals
        if visited_nodes.get((current[0],tuple(current[1])))==None:
            visited_nodes[(current[0],tuple(current[1]))]=1
           # print(currentpath)
            if current[0] in current[1]:#current[0]-->node coordinates
                current[1].remove(current[0])
                if len(current[1])==0:
                    return currentpath
            for i in maze.getNeighbors(current[0][0],current[0][1]):
                if visited_nodes.get((i,tuple(current[1])))==None:
                    heapq.heappush(fringe, (heuristic1(i,current[1].copy(),len(current[1]))+cost, (i,current[1].copy()), currentpath+[i],cost+1))
'''def fast(maze: Maze):
    start: tuple=maze.getStart()
    path=[]
    visit=dict()
    
    return dfs(maze,start,path,visit,maze.getObjectives())[0]
def dfs(maze: Maze,node,path,visit,goals):
    #print(path)
    if node not in visit:
        visit[(node[0],node[1])]=1
        path=path+[node]
        for dot in maze.getNeighbors(node[0],node[1]):
            if dot in goals:
                goals.remove(dot)
            if dot not in visit:
                path,goals=dfs(maze,dot,path,visit,goals)
                if len(goals)!=0:
                    path=path+[node]
    return path,goals'''