# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 21:59:20 2022

@author: Roger Luo
"""
from GenProcesses import *
import copy

def SRT(Processes, contextSwitch, alpha):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    Q = [] #The Queue
    time = 0 #The number of milliseconds that has passed
    preemptions = 0
    Working = False
    procLeft = Processes.num_process_
    arrTime = Processes.arrival_Time
    procCopy = copy.deepcopy(Processes.reorganizedData)

    print("time 0ms: Simulator started for SRT ", end = "")
    printQueue(Q)
    