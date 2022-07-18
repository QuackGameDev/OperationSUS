# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 21:59:20 2022

@author: Roger Luo
"""
from GenProcesses import *
import copy


    
def SRT(Processes, contextSwitch, alpha):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    processesInfo = Processes.reorganizedData
    Q = [] #The Queue
    time = 0 #The number of milliseconds that has passed
    preemptions = 0
    procLeft = Processes.num_process_
    arrTime = Processes.arrival_Time
    cpuBursts = copy.deepcopy(Processes.CPU_Burst)
    ioBursts = copy.deepcopy(Processes.IO_Burst)
    numBursts = copy.deepcopy(Processes.num_Burst)
    taus = [Processes.tau for x in range(procLeft)]
    CPU_burst=True
    CPU = []
    completed = [] #Which processes are done
    IO = [] #What is in the IO
    IO_R = []
    P = [] # Preempting
    cSwitches = 0 #The number of times that context switching occurs
    buffer = contextSwitch
    Working = False
    CPU_burst_timer =0 

    def sortQueue(e):
        return processesInfo.get(e).get("tau"),ord(e)

    print("time 0ms: Simulator started for SRT ", end = "")
    printQueue(Q)
    while(len(completed)<Processes.num_process_):
        for x in arrTime:
            if(x == time):
                Q.append(alphabet[arrTime.index(x)])
                Q.sort(key = sortQueue)
                print("time ", time, "ms: Process ", alphabet[arrTime.index(x)], " (tau ", taus[arrTime.index(x)], "ms) arrived; added to ready queue ", end = "", sep = "")
                printQueue(Q)
        
        #Checking if there is nothing in the CPU Burst Queue and putting something if there is something
        if(CPU_burst==False):
            buffer = contextSwitch
            CPU.append(Q[0])
            CPU_burst = True

        

        # Must make a preempting branch just in case in order to print those that are remaining if any processes have been preempted
        if ( CPU_burst == True and buffer ==0 and len(P)>0):
            if(CPU[0] == P[0][0]):

            else:
                

        #After the context switch has finished and CPU Burst has been activateed
        elif(CPU_burst == True and buffer == 0 and len(P)==0):
            print("time ", time, "ms: Process ", alphabet[arrTime.index(x)], " (tau ", taus[arrTime.index(x)], "ms) arrived; added to ready queue ", end = "", sep = "")
            CPU_burst_timer = 
       

        #Check if CPU Burst timer has reached 0 and starts moving it into the IO Queue, must make branches for either if the last CPU Burst or second to last CPU Burst for the Process
        if(CPU_burst_timer == 0 and CPU_burst == True):

        #Checking if any IO Bursts are done and then start moving them into standby procedure for moving them back into the ready queue
        if(len(IO)>0):

        #Moving those that are in standby from IO queue to ready queue.
        if(len(IO_R)>0):
            for i in IO:
                #Preempting check if Tau -CPU Burst time that's already been used is bigger than the tau that's just been freed from the IO Queue
                if()


        CPU_burst_timer-=1
        buffer -= 1
        time += 1
    print("")