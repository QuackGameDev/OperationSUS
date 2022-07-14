# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 21:59:20 2022

@author: Quang Nguyen
"""
from GenProcesses import *
# this function will give back all occurence of the targetNum in a list
# always give back a list that is ordered from samllest to biggest index
def allIndexOfTargerNum(targetNum, list):
    allIndex = []
    for i in range(len(list)):
        if (targetNum == list[i]):
            allIndex.append(i)
            
    return allIndex

# parameter: pass in a Processes class

def FCFS(Processes, contextSwitchTime):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # tell whenever the algo is done so the timer stop
    allProcessTerminate = False
    
    # In charge of how many processes
    numProcess = Processes.self.num_process_ 
    
    # a LIST that keep track of the time that the next process arrive. Pop arrival_Time[0] out once timer = arrival_Time[0]
    arrivalTimer = Processes.self.arrival_Time
    
    # a dict of all of the info of all processes
    processesInfo = Processes.self.reorganizedData
    
    
    
    
    # list of processes in the ready queue
    ready_queue = []
    
    # list of processes in the IO Burst State
    IOqueue = []
    
    # list of processes in the CPU Burst State
    CPUqueue = []
    
    # list of processes finish both IO and CPU Burst
    completed = []
    
    print("time 0ms: Simulator started for FCFS [Q: empty]")
    timer  = 0
    while(not allProcessTerminate):
        # if there are still Processes left to arrive, print that out
        processesNameList = allIndexOfTargerNum(timer, arrivalTimer)
        if(numProcess > 0 and len(processesNameList) > 0):
            # add all of the processes to the queue
            for i in range(len(processesNameList)):
                ready_queue.append()
        
        
        
        
        timer += 1
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    test_Process = Processes(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]))
    test_Process.generateProcesses()
    test_Process.reorganizeData()
    test_Process.printReorganizedData()
    