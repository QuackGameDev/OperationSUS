# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 21:59:20 2022

@author: Quang Nguyen, Roger Luo
"""
# parameter: pass in a Processes class
def RR(processes, contextSwitchTime, timeSlice):
    queue = []
    processing = []
    completed = []
    allCompleted = False # keep track of when all of the processes is completed or not
    arrTime = Processes.arrival_Time
    cpuBursts = copy.deepcopy(Processes.CPU_Burst)
    ioBursts = copy.deepcopy(Processes.IO_Burst)
    numBursts = copy.deepcopy(Processes.num_Burst)
    cSwitches = 0 #The number of times that context switching occurs
    print("time 0ms: Simulator started for RR with time slice {ts}ms [Q: empty]".format(ts = timeSlice))
    timer = 0