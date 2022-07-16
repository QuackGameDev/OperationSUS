# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 21:59:20 2022

@author: Roger Luo
"""
from GenProcesses import *
import copy

def add2Q(Q, Process):
    Q.append(Process)
    
def SRT(Processes, contextSwitch, alpha):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    Q = [] #The Queue
    time = 0 #The number of milliseconds that has passed
    preemptions = 0
    procLeft = Processes.num_process_
    arrTime = Processes.arrival_Time
    procCopy = copy.deepcopy(Processes.reorganizedData)
    AllDone = False
    completed = [] #Which processes are done
    IO = [] #What is in the IO
    cSwitches = 0 #The number of times that context switching occurs


    print("time 0ms: Simulator started for SRT ", end = "")
    printQueue(Q)
