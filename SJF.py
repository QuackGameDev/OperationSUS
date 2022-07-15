"""
Created on Thu Jul 14 19:54:41 2022

@author: Raphael Chung
notes:
- The ready Queue must be sorted by CPU Burst time
- Whenever a Process Completes a CPU Burst, Tau must be recalculated
- When the ready queue is empty, it must say [Q: empty]
- Each process has it's own burst
- total turnaround time = total burst time + total wait time + (number of context switches * time for each context switch)

- After you simulate each scheduling algorithm, you must reset the simulation back to the initial
set of processes and set your elapsed time back to zero. More specifically, you must re-seed your
random number generator to ensure the same set of processes and interarrival times
- How to "eliminate" Bursts when done?
- Do we eliminate the first part of the Queue when done with it?
F
"""
from GenProcesses import *

def allIndexOfTargerNum(targetNum, list):
    allIndex = []
    for i in range(len(list)):
        if (targetNum == list[i]):
            allIndex.append(i)
            
    return allIndex

def SJF(Processes, contextSwitchTime):
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
    
    print("time 0ms: Simulator started for SJF [Q: empty]")
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
    print("yeeet")
    test_Process = Processes(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]))
    test_Process.generateProcesses()
    test_Process.reorganizeData()
    test_Process.printReorganizedData()
    #test_Process.print()

