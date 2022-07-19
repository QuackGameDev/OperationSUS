# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 21:59:20 2022

@author: Roger Luo
"""
from GenProcesses import *
import copy
import math
    
def SRT(Processes, contextSwitch, alpha):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    processesInfo = Processes.reorganizedData
    Q = [] #The Queue
    time = 0 #The number of milliseconds that has passed
    preemptions = 0
    procLeft = Processes.num_process_
    arrTime = Processes.arrival_Time
    cpuBursts = copy.deepcopy(Processes.CPU_Burst)
    oriBursts = Processes.CPU_Burst
    ioBursts = copy.deepcopy(Processes.IO_Burst)
    numBursts = copy.deepcopy(Processes.num_Burst)
    taus = [Processes.tau for x in range(procLeft)]
    CPU_burst = False
    currBurst = [0 for x in range(procLeft)] #Keeps track of which burst the processes are in
    CPU = []
    completed = [] #Which processes are done
    IO = [] #What is in the IO
    IO_R = []
    P = [] # Preempting
    cSwitches = 0 #The number of times that context switching occurs
    buffer = contextSwitch/2

    buffQueue = []
    toReady = []
    readyBuff = 0
    ioBuff = 0
    ioOut = []
    prepreempt = copy.deepcopy(taus)
    
    """Stats variable"""
    avgCPUBurstTime = calAvgCPUBurstTime(Processes)
    
    
    # list of the total wait time to calculate average wait time
    waittime = 0
    
    # list of the total turnaround time to calculate average turnaround time
    turntime = 0
    avgTurn=[]
    # Keep track of number of context switches
    numContextSwitch = 0
    
    stats = []


    def sortQueue(e):
        return prepreempt[alphabet.index(e)],ord(e)

    print("time 0ms: Simulator started for SRT ", end = "")
    printQueue(Q)
    while(len(completed)<Processes.num_process_):
        for x in arrTime:
            if(x == time):
                Q.append(alphabet[arrTime.index(x)])
                Q.sort(key = sortQueue)
                print("time ", time, "ms: Process ", alphabet[arrTime.index(x)], " (tau ", taus[arrTime.index(x)], "ms) arrived; ", end = "", sep = "")
                
                if(len(CPU) > 0):
                    if(  taus[alphabet.index(CPU[0])] - (oriBursts[alphabet.index(CPU[0])][currBurst[alphabet.index(CPU[0])]] - cpuBursts[alphabet.index(CPU[0])][currBurst[alphabet.index(CPU[0])]])  > taus[arrTime.index(x)]):
                        print("preempting ", CPU[0], " ", end = "", sep = "")
                        prepreempt[alphabet.index(CPU[0])] = currStart
                        readyBuff = contextSwitch/2
                        toReady.append(CPU[0])
                        prepreempt[alphabet.index(CPU[0])] = taus[alphabet.index(CPU[0])] - (oriBursts[alphabet.index(CPU[0])][currBurst[alphabet.index(CPU[0])]] - cpuBursts[alphabet.index(CPU[0])][currBurst[alphabet.index(CPU[0])]])
                        CPU.pop()
                        CPU_burst = False
                        preemptions +=1
                    else:
                        print("added to ready queue ", end = "", sep = "")
                else:
                    print("added to ready queue ", end = "", sep = "")
                printQueue(Q)
        
        if(ioBuff > 0):
            ioBuff-=1

        #Check if CPU Burst timer has reached 0 and starts moving it into the IO Queue, must make branches for either if the last CPU Burst or second to last CPU Burst for the Process
        if(CPU_burst == True):
            cpuBursts[alphabet.index(CPU[0])][currBurst[alphabet.index(CPU[0])]] -= 1
            if(cpuBursts[alphabet.index(CPU[0])][currBurst[alphabet.index(CPU[0])]] == 0):
                CPU_burst = False
                currBurst[alphabet.index(CPU[0])] += 1
                burstLeft = numBursts[alphabet.index(CPU[0])] - currBurst[alphabet.index(CPU[0])]
                if(burstLeft == 0):
                    print("time ", time, "ms: Process ", CPU[0], " terminated ", end = "", sep = "")
                    printQueue(Q)
                    procLeft -=1
                    completed.append(CPU[0])
                    avgTurn.append(time - arrTime[alphabet.index(CPU[0])])
                    CPU.pop()
                    if(len(Q) > 0):
                        buffer = contextSwitch
                    if(procLeft == 0):
                        break
                else:
                    if(time <= 1000):
                        if(burstLeft > 1):
                            print("time ", time, "ms: Process ", CPU[0], " (tau ", taus[alphabet.index(CPU[0])], "ms) completed a CPU burst; ", burstLeft, " bursts to go ", end = "", sep = "")
                        else:
                            print("time ", time, "ms: Process ", CPU[0], " (tau ", taus[alphabet.index(CPU[0])], "ms) completed a CPU burst; 1 burst to go ", end = "", sep = "")
                        printQueue(Q)
                    
                    old_tau = taus[alphabet.index(CPU[0])]
                    actual_burst = oriBursts[alphabet.index(CPU[0])][currBurst[alphabet.index(CPU[0])] - 1]
                    taus[alphabet.index(CPU[0])] = int(math.ceil(alpha * actual_burst +(1-alpha) * old_tau))
                    prepreempt[alphabet.index(CPU[0])] = taus[alphabet.index(CPU[0])]
                    if(time <= 1000):
                        print("time "+str(time)+"ms: Recalculated tau for process "+str(CPU[0])+": old tau "+str(old_tau)+"ms; new tau "+str(taus[alphabet.index(CPU[0])])+"ms ", end = "", sep = "" )
                        printQueue(Q)

                        print("time ", time, "ms: Process ", CPU[0], " switching out of CPU; will block on I/O until time ", 
                        int(time + int(ioBursts[alphabet.index(CPU[0])][currBurst[alphabet.index(CPU[0])] - 1]) + contextSwitch/2),"ms " , end = "", sep = "")
                        printQueue(Q)
                    cSwitches+=1


                    ioOut.append(int(time + int(ioBursts[alphabet.index(CPU[0])][currBurst[alphabet.index(CPU[0])] - 1]) + contextSwitch/2))

                    IO.append(CPU[0])
                    ioBuff = contextSwitch/2
                    if(len(Q) > 0):
                        buffer = contextSwitch/2 
                    CPU.pop()
        if(buffer == 0): #After the context switch buffer, add things into the CPU
            buffer = contextSwitch/2
            CPU.append(buffQueue[0])
            buffQueue.pop(0)
            currStart = time
            CPU_burst = True
            oriTime = oriBursts[alphabet.index(CPU[0])][currBurst[alphabet.index(CPU[0])]]
            if(oriTime == cpuBursts[alphabet.index(CPU[0])][currBurst[alphabet.index(CPU[0])]]):
                if(time <= 1000):
                    print("time ", time, "ms: Process ", CPU[0], " (tau ", taus[alphabet.index(CPU[0])], "ms) started using the CPU for ",
                    int(cpuBursts[alphabet.index(CPU[0])][currBurst[alphabet.index(CPU[0])]]),"ms burst ", end = "", sep = "")
            else:
                if(time <= 1000):
                    print("time ", time, "ms: Process ", CPU[0], " (tau ", taus[alphabet.index(CPU[0])], "ms) started using the CPU for remaining ", 
                    int(cpuBursts[alphabet.index(CPU[0])][currBurst[alphabet.index(CPU[0])]]),"ms of ", oriTime, "ms burst ", end = "", sep = "")
            if(time <= 1000):
                printQueue(Q)
            if(len(Q) > 0):
                if(  taus[alphabet.index(CPU[0])] - (oriBursts[alphabet.index(CPU[0])][currBurst[alphabet.index(CPU[0])]] - cpuBursts[alphabet.index(CPU[0])][currBurst[alphabet.index(CPU[0])]])  > taus[alphabet.index(Q[0])]):
                    print("time ", time, "ms: Process ", Q[0], " (tau ", taus[alphabet.index(Q[0])], "ms) will preempt ", CPU[0], " ",  end = "", sep = "")
                    printQueue(Q)
                    prepreempt[alphabet.index(CPU[0])] = currStart
                    readyBuff = contextSwitch/2
                    toReady.append(CPU[0])
                    prepreempt[alphabet.index(CPU[0])] = taus[alphabet.index(CPU[0])] - (oriBursts[alphabet.index(CPU[0])][currBurst[alphabet.index(CPU[0])]] - cpuBursts[alphabet.index(CPU[0])][currBurst[alphabet.index(CPU[0])]])
                    CPU.pop()
                    CPU_burst = False
                    preemptions +=1



        #Checking if any IO Bursts are done and then start moving them into standby procedure for moving them back into the ready queue
        if(len(IO)>0):
            x = 0
            ioDone = []
            while(x < len(IO)):
                if(time == ioOut[x]):
                    ioDone.append(IO[x])
                    ioOut.pop(x)
                    IO.pop(x)
                    x-=1
                x+=1

            if(len(ioDone) > 0):
                ioDone.sort()
                for x in ioDone:
                    Q.append(x)
                    if(time <= 1000):
                        print("time ", time, "ms: Process ", x , " (tau ", taus[alphabet.index(x)], "ms) completed I/O;",end = "", sep = "")
                    if(len(CPU) > 0):

                        if( taus[alphabet.index(CPU[0])] - (oriBursts[alphabet.index(CPU[0])][currBurst[alphabet.index(CPU[0])]] - cpuBursts[alphabet.index(CPU[0])][currBurst[alphabet.index(CPU[0])]]) > taus[alphabet.index(x)]):
                            if(time <= 1000):
                                print(" preempting ", CPU[0], " ", end = "", sep = "")
                            readyBuff = contextSwitch/2
                            prepreempt[alphabet.index(CPU[0])] = taus[alphabet.index(CPU[0])] - (oriBursts[alphabet.index(CPU[0])][currBurst[alphabet.index(CPU[0])]] - cpuBursts[alphabet.index(CPU[0])][currBurst[alphabet.index(CPU[0])]])
                            toReady.append(CPU[0])
                            CPU.pop()
                            CPU_burst = False
                            preemptions +=1
                        else:
                            if(time <= 1000):
                                print(" added to ready queue ", end = "", sep = "")
                    else:
                        if(time <= 1000):
                            print(" added to ready queue ", end = "", sep = "")
                    Q.sort(key = sortQueue)
                    if(time <= 1000):
                        printQueue(Q)
                ioDone.clear()

        if(len(CPU) == 0 and len(toReady) == 0 and ioBuff == 0):
            if(len(Q) > 0 ):
                buffer -= 1
                if(buffer == contextSwitch/4 and len(buffQueue) == 0):
                    buffQueue.append(Q[0])
                    Q.pop(0)
            elif(len(buffQueue) == 1):
                buffer-=1
        
        if(len(toReady) == 1):
            readyBuff -=1
            if(readyBuff == 0):
                Q.append(toReady[0])
                toReady.pop(0)
                Q.sort(key = sortQueue)
                
        waittime+= (len(Q) * 1)
        time += 1
    time += contextSwitch/2
    print("time "+str(int(time))+"ms: Simulator ended for SRT ",end = "", sep = "")
    waittime = waittime/Processes.num_process_
    for x in avgTurn:
        turntime+=x
    turntime = turntime/Processes.num_process_
    
    CPUUtilNum = ceil(((calcTotalCPUTime(Processes) / time) * 100) * 1000)/1000    
    stats.append("SRT")
    stats.append(avgCPUBurstTime)
    stats.append(waittime)
    stats.append(turntime)
    stats.append(cSwitches)
    stats.append(preemptions)
    stats.append(CPUUtilNum)
    
    printQueue(Q)
    return stats



if __name__ == "__main__":
    test_Process = Processes(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]))
    test_Process.generateProcesses()
    test_Process.reorganizeData()
    SRT(test_Process, int(sys.argv[5]), float(sys.argv[6]))