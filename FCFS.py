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
    """Deep copy the Processes so I can fuck around with without changing the original version"""
    
    
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # tell whenever the algo is done so the timer stop
    allProcessTerminate = False
    
    # In charge of how many processes
    numProcessLeft = Processes.num_process_ 
    
    # a LIST that keep track of the time that the next process arrive. Pop arrival_Time[0] out once timer = arrival_Time[0]
    arrivalTimer = Processes.arrival_Time
    
    # a dict of all of the info of all processes
    processesInfo = Processes.reorganizedData
    
    # list of processes in the ready queue
    ready_queue = []
    
    # list of processes in the CPU Burst State
    CPUqueue = []
    
    # list of processes in the IO Burst State
    IOqueue = []
    
    # list of processes finish both IO and CPU Burst
    completed = []
    
    print("time 0ms: Simulator started for FCFS [Q: empty]")
    timer = 0
    
    startcontextSwitch = contextSwitchTime / 2
    endcontextSwitch = contextSwitchTime / 2
    
    startContextSwitchCountdown = False
    endContextSwitchCountdown = False
    
    CPUBurstTimeRemain = 0
    
    while(not allProcessTerminate):
        # if there are still Processes left to arrive, print that out
        processesNameList = allIndexOfTargerNum(timer, arrivalTimer)
        # if there are still processes left to add and len of proccesses need to add at that specific time is bigger than 0
        if(numProcessLeft > 0 and len(processesNameList) > 0):
            # add all of the processes to the queue
            for i in processesNameList:
                ready_queue.append(alphabet[i])
                info = "time {time}ms: Process {processName} arrived; added to ready queue [Q:".format(time = timer, processName = alphabet[i])
                for j in ready_queue:
                    info += " {name}".format(name = j)
                info += "]"
                print(info)
                startContextSwitchCountdown = True
                numProcessLeft -= 1 # subtract all of the processes that has already arrive so we don't add in more duplicate processes.
                
        
        # You don't need a CPUBurst queue cuz the Processes have to wait until the prev processes finished
        
        if(startContextSwitchCountdown):
            startcontextSwitch -= 1
        # Now to the CPU and IO Burst     
        # Process only start CPU burst only when its finish the IO burst and got shove back into the
        # ready queue  
        if(startcontextSwitch == 0):
            # Do CPU Burst
            CPUBurstTime = processesInfo.get(ready_queue[0]).get("CPUBurst")[processesInfo.get(ready_queue[0]).get("currentBurstIndex")]
            CPUBurstTimeRemain = timer + CPUBurstTime
            CPUqueue.append(ready_queue[0])
            ready_queue.pop(0)
            
            info = "time {time}ms: Process {processName} started using the CPU for {CPUburst}ms burst [Q:".format(time = timer, processName = ready_queue[0], CPUburst = CPUBurstTime)
            if(len(ready_queue) == 0):
                info += " empty]"
                print(info)
            else:
                for j in ready_queue:
                    info += " {name}".format(name = j)
                info += "]"
                print(info)
            
            
            startcontextSwitch = contextSwitchTime / 2 # reset the context switch time
            startContextSwitchCountdown = False
        
        
        if(timer == CPUBurstTimeRemain):
            endContextSwitchCountdown = True   
            CPUBurstTimeRemain = 0 # reset CPU burst time 
        if(endContextSwitchCountdown):
            endcontextSwitch -= 1
            
            
            
        if(endContextSwitchCountdown == 0 and timer == CPUqueue[0][0]):
            numBurstLeft = processesInfo.get(CPUqueue[0][1]).get("numBurst")
            if(numBurstLeft > 1):
                # Do IO Burst (loop through the entire CPU queue to see if any process have the same CPU burst finish time)
                numBurstLeft = processesInfo.get(CPUqueue[0][1]).get("numBurst") - 1
                # formnat of the list: [CPU Burst ending time, Process Name]
                info = "time {time}ms: Process {processName} completed a CPU burst; {burstLeft} bursts to go [Q:".format(time = timer, 
                                                                                                                         processName = CPUqueue[0][1],
                                                                                                                         burstLeft = numBurstLeft)
                if(len(ready_queue) == 0):
                    info += " empty]"
                    print(info)
                    info = ""
                else:
                    for j in ready_queue:
                        info += " {name}".format(name = j)
                    info += "]"
                    print(info)
                    info = ""

                # reduce num Burst by one
                # CPUqueue[0][1] = process name
                processesInfo.get(CPUqueue[0][1])["numBurst"] = numBurstLeft
                
                # print out messages
                # create IO burst end time (timer + end time + (contextswitch / 2)) and name of process
                # add info into IO Burst queue
                
                
                
                
            
            
            
                endcontextSwitch = contextSwitchTime / 2
                endContextSwitchCountdown = False
            
            # subtract numBurst by one after finish CPU queue
            
            
        # if a IO burst is finished, add the process back into ready queue
        # increment currentBurstIndex by one for the processes and continue processing
        
        
        
        # if a process's currentBurstIndex = numBurst, processes is completed, move to allCompleted
        
        
        
        
        
        # if every processes already been "process"
        if(len(completed) == Processes.num_process_):
            allProcessTerminate = True
        
        timer += 1
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    test_Process = Processes(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]))
    test_Process.generateProcesses()
    test_Process.reorganizeData()
    test_Process.printReorganizedData()
    #FCFS(test_Process, 0)