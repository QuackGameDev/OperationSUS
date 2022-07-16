# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 21:59:20 2022

@author: Quang Nguyen, Roger Luo
"""

from GenProcesses import *
import copy

# parameter: pass in a Processes class
def RR(Processes, contextSwitchTime, timeSlice):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    Q = []
    processing = []
    completed = []

    allCompleted = False # keep track of when all of the processes is completed or not
    procLeft = Processes.num_process_
    arrTime = Processes.arrival_Time
    cpuBursts = copy.deepcopy(Processes.CPU_Burst)
    ioBursts = copy.deepcopy(Processes.IO_Burst)
    numBursts = copy.deepcopy(Processes.num_Burst)
    currBurst = [] #Keeps track of which burst the processes are in
    IO = [] #What is in the IO
    cSwitches = 0 #The number of times that context switching occurs
    buffer = contextSwitchTime
    
    print("time 0ms: Simulator started for RR with time slice {ts}ms [Q: empty]".format(ts = timeSlice))
    time = 0

    while(procLeft > 0):
        for x in arrTime:
            if(x == time):
                Q.append(alphabet[arrTime.index(x)])
                print("time ", time, "ms: Process ", alphabet[arrTime.index(x)], " arrived; added to ready queue ", end = "", sep = "")
                printQueue(Q)
                procLeft -=1
        time += 1
    print("")