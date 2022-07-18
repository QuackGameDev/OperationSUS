# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 21:59:20 2022

@author: Quang Nguyen
notes:
Layout and "if" conditions inspired/provided by Raphael Chung
"""
from GenProcesses import *
import copy
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
    tempProcesses = copy.copy(Processes)
    
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # tell whenever the algo is done so the timer stop
    allProcessTerminate = False
    
    # In charge of how many processes left
    numProcessLeft = tempProcesses.num_process_ 
    
    # a LIST that keep track of the time that the next process arrive. Pop arrival_Time[0] out once timer = arrival_Time[0]
    arrivalTimer = tempProcesses.arrival_Time
    
    # a dict of all of the info of all processes
    processesInfo = tempProcesses.reorganizedData
    
    # list of processes in the ready queue
    ready_queue = []
    
    # list of processes in the CPU Burst State
    CPUqueue = []
    
    # list of processes in the IO Burst State (processes name) 
    IOQueue = []
    
    # list of processes finish both IO and CPU Burst
    completed = []
    
    # The transfer between IO to ready queue, holds the time in which they re enter.
    IO_to_ready = []
    
    # Context switch time    
    contextSwitch = contextSwitchTime / 2
    
    # keep in charge of when a process enters CPU Burst
    CPUBurst = False

    # keep in charge of when to switch context
    timerToSwitch = -1

    # keep in charge of when CPU Burst Time ran out
    CPUBurstTimer = -1
    
    print("time 0ms: Simulator started for FCFS [Q: empty]")
    timer = 0
    
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
                # if CPUqueue is empty, then you start context switch timer
                # so you can start doing CPU Burst, or else there is still CPU Burst ahead
                numProcessLeft -= 1 # subtract all of the processes that has already arrive so we don't add in more duplicate processes.
        
        
        # finish CPU Burst, time for IO Burst
        if (CPUBurst == True and CPUBurstTimer == 0):
            if (len(processesInfo.get(CPUqueue[0]).get("CPUBurst")) - processesInfo.get(CPUqueue[0]).get("currentBurstIndex") - 1) == 0:
                info = "time {time}ms: Process {processName} terminated [Q:".format(time = timer,
                                                                                    processName = CPUqueue[0])
                if(len(ready_queue) == 0):
                    info += " empty]"
                    print(info)
                else:
                    for j in ready_queue:
                        info += " {name}".format(name = j)
                    info += "]"
                    print(info)
                completed.append(CPUqueue[0])
                CPUqueue.pop(0)
                timerToSwitch = contextSwitch
                CPUBurst = False
            else:
                numBurstLeft = processesInfo.get(CPUqueue[0]).get("numBurst")
                # Do IO Burst (loop through the entire CPU queue to see if any process have the same CPU burst finish time)
                numBurstLeft -= 1
                # formnat of the list: [CPU Burst ending time, Process Name]
                if(numBurstLeft == 1):
                    info = "time {time}ms: Process {processName} completed a CPU burst; {burstLeft} burst to go [Q:".format(time = timer, 
                                                                                                                         processName = CPUqueue[0],
                                                                                                                         burstLeft = numBurstLeft)
                else:
                    info = "time {time}ms: Process {processName} completed a CPU burst; {burstLeft} bursts to go [Q:".format(time = timer, 
                                                                                                                         processName = CPUqueue[0],
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

                # reduce and update num Burst by one
                # CPUqueue[0] = process name
                processesInfo.get(CPUqueue[0]).update({"numBurst": numBurstLeft})
                
                IOBurstEndTime = timer + processesInfo.get(CPUqueue[0]).get("IOBurst")[processesInfo.get(CPUqueue[0]).get("currentBurstIndex")] + (contextSwitchTime / 2)
                # print out messages
                info = "time {time}ms: Process {processName} switching out of CPU; will block on I/O until time {IOEndTime}ms [Q:".format(time = timer, 
                                                                                                                                          processName = CPUqueue[0], 
                                                                                                                                          IOEndTime = int(IOBurstEndTime))
                if(len(ready_queue) == 0):
                    info += " empty]"
                else:
                    for j in ready_queue:
                        info += " {name}".format(name = j)
                    info += "]"
                
                print(info)
                IOQueue.append([IOBurstEndTime, CPUqueue[0]])
                CPUqueue.pop(0)
                timerToSwitch = contextSwitch
                CPUBurst = False
        
        # IO Burst finished, add CPU back to the ready queue
        # This activates only if IO queue has any processes inside.
        if(len(IOQueue) > 0):
            i=0
            while i < len(IOQueue):
                if(IOQueue[i][0] == timer):
                    IO_to_ready.append(IOQueue[i])
                    IOQueue.remove(IOQueue[i])
                    i -= 1
                i += 1
        
        
        # Time to start CPU Burst
        if (CPUBurst == True and timerToSwitch == 0):
            CPUBurstTimer = processesInfo.get(CPUqueue[0]).get("CPUBurst")[processesInfo.get(CPUqueue[0]).get("currentBurstIndex")]
            info = "time {time}ms: Process {processName} started using the CPU for {CPUBurst}ms burst [Q:".format(time = timer, 
                                                                                                                  processName = CPUqueue[0], 
                                                                                                                  CPUBurst = int(CPUBurstTimer))
            if(len(ready_queue) == 0):
                info += " empty]"
                print(info)
            else:
                for j in ready_queue:
                    info += " {name}".format(name = j)
                info += "]"
                print(info)
        
        
        
        # This activates only if there are processes just waiting to head into ready queue from IO queue
        if(len(IO_to_ready) > 0):
            i=0
            while i < (len(IO_to_ready)):
                if(IO_to_ready[i][0] == timer):
                    ready_queue.append(IO_to_ready[i][1])
                    info = "time {time}ms: Process {processName} completed I/O; added to ready queue [Q:".format(time = timer, 
                                                                                                        processName = IO_to_ready[i][1])
                    if(len(ready_queue) == 0):
                        info += " empty]"
                        print(info)
                    else:
                        for j in ready_queue:
                            info += " {name}".format(name = j)
                        info += "]"
                        print(info)
                    
                    processesInfo.get(IO_to_ready[i][1])["currentBurstIndex"] += 1
                    IO_to_ready.pop(i)
                    i -= 1
                i += 1
        
        # if ready queue is loaded up, start 
        if(CPUBurst == False and len(ready_queue) > 0 and timerToSwitch <= 0):
            CPUqueue.append(ready_queue[0])
            ready_queue.pop(0)
            CPUBurst = True
            timerToSwitch = contextSwitch
        
        
        
        if(len(completed) == tempProcesses.num_process_):
            allProcessTerminate = True
            info = "time {time}ms: Simulator ended for FCFS [Q: empty]".format(time = timer + 2)
            print(info, end = "")
        
        CPUBurstTimer -= 1
        timerToSwitch -= 1
        timer += 1
    
    
if __name__ == "__main__":
    test_Process = Processes(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]))
    test_Process.generateProcesses()
    test_Process.reorganizeData()
    #test_Process.printReorganizedData()
    FCFS(test_Process, int(sys.argv[5]))