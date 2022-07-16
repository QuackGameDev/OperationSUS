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
    procLeft = Processes.num_process_
    arrTime = Processes.arrival_Time
    cpuBursts = copy.deepcopy(Processes.CPU_Burst)
    ioBursts = copy.deepcopy(Processes.IO_Burst)
    numBursts = copy.deepcopy(Processes.num_Burst)
    taus = [Processes.tau for x in range(procLeft)]
    AllDone = False
    Curr = "" #The current process the CPU is working on
    completed = [] #Which processes are done
    IO = [] #What is in the IO
    cSwitches = 0 #The number of times that context switching occurs
    buffer = contextSwitch

    print("time 0ms: Simulator started for SRT ", end = "")
    printQueue(Q)
    while(procLeft > 0):
        for x in arrTime:
            if(x == time):
                Q.append(alphabet[arrTime.index(x)])
                print("time ", time, "ms: Process ", alphabet[arrTime.index(x)], " (tau ", taus[arrTime.index(x)], "ms) arrived; added to ready queue ", end = "", sep = "")
                printQueue(Q)
        if(buffer == 0):
            buffer = contextSwitch
            Working = True

        if(Working == False):
            buffer -= 1
            continue
    
        time += 1