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

    procLeft = Processes.num_process_
    arrTime = Processes.arrival_Time
    cpuBursts = copy.deepcopy(Processes.CPU_Burst)
    oriBursts = Processes.CPU_Burst
    ioBursts = copy.deepcopy(Processes.IO_Burst)
    numBursts = copy.deepcopy(Processes.num_Burst)
    currBurst = [0 for x in range(procLeft)] #Keeps track of which burst the processes are in
    IO = [] #What is in the IO
    ioOut = []
    cSwitches = 0 #The number of times that context switching occurs
    buffer = contextSwitchTime/2
    currStart = 0 #Keeps track of when the current process has started
    preemptions = 0
    buffQueue = []
    toReady = []
    readyBuff = 0

    #Beginning of Algorithm
    print("time 0ms: Simulator started for RR with time slice {ts}ms [Q: empty]".format(ts = timeSlice))
    time = 0

    while(procLeft > 0):

        for x in arrTime: #Add the processes slowly by arrival times
            if(x == time):
                Q.append(alphabet[arrTime.index(x)])
                print("time ", time, "ms: Process ", alphabet[arrTime.index(x)], " arrived; added to ready queue ", end = "", sep = "")
                printQueue(Q)



        if(len(processing) == 1):
            cpuBursts[alphabet.index(processing[0])][currBurst[alphabet.index(processing[0])]] -= 1
            if(cpuBursts[alphabet.index(processing[0])][currBurst[alphabet.index(processing[0])]] == 0):
                currBurst[alphabet.index(processing[0])] += 1
                burstLeft = numBursts[alphabet.index(processing[0])] - currBurst[alphabet.index(processing[0])]
                if(burstLeft == 0):
                    print("time ", time, "ms: Process ", processing[0], " terminated ", end = "", sep = "")
                    printQueue(Q)
                    procLeft -=1
                    completed.append(processing[0])
                    processing.pop()
                    if(len(Q) > 0):
                        buffer = contextSwitchTime
                    if(procLeft == 0):
                        break
                else:
                    if(burstLeft > 1):
                        print("time ", time, "ms: Process ", processing[0], " completed a CPU burst; ", burstLeft, " bursts to go ", end = "", sep = "")
                    else:
                        print("time ", time, "ms: Process ", processing[0], " completed a CPU burst; 1 burst to go ", end = "", sep = "")
                    printQueue(Q)
                    print("time ", time, "ms: Process ", processing[0], " switching out of CPU; will block on I/O until time ", int(time + int(ioBursts[alphabet.index(processing[0])][currBurst[alphabet.index(processing[0])] - 1]) + contextSwitchTime/2),"ms " , end = "", sep = "")
                    ioOut.append(int(time + int(ioBursts[alphabet.index(processing[0])][currBurst[alphabet.index(processing[0])] - 1]) + contextSwitchTime/2))
                    printQueue(Q)
                    IO.append(processing[0])
                    if(len(Q) > 0):
                        buffer = contextSwitchTime
                    processing.pop()

            if(len(processing) == 1):
                if((time - currStart)%timeSlice == 0):
                    if(len(Q) == 0):
                        print("time ", time, "ms: Time slice expired; no preemption because ready queue is empty ",end = "", sep = "")
                        printQueue(Q)
                    else:
                        print("time ", time, "ms: Time slice expired; process ", processing[0], " preempted with ", int(cpuBursts[alphabet.index(processing[0])][currBurst[alphabet.index(processing[0])]]) , "ms remaining ",end = "", sep = "")
                        printQueue(Q)
                        readyBuff = contextSwitchTime/2
                        toReady.append(processing[0])
                        processing.pop()
                        preemptions += 1
                

        if(buffer == 0): #After the context switch buffer, add things into the CPU
            buffer = contextSwitchTime/2
            processing.append(buffQueue[0])
            buffQueue.pop(0)
            cSwitches +=1
            currStart = time
            oriTime = oriBursts[alphabet.index(processing[0])][currBurst[alphabet.index(processing[0])]]
            if(oriTime == cpuBursts[alphabet.index(processing[0])][currBurst[alphabet.index(processing[0])]]):
                print("time ", time, "ms: Process ", processing[0], " started using the CPU for ", int(cpuBursts[alphabet.index(processing[0])][currBurst[alphabet.index(processing[0])]]),"ms burst ", end = "", sep = "")
            else:
                print("time ", time, "ms: Process ", processing[0], " started using the CPU for remaining ", int(cpuBursts[alphabet.index(processing[0])][currBurst[alphabet.index(processing[0])]]),"ms of ", oriTime, "ms burst ", end = "", sep = "")
            printQueue(Q)
        
        x = 0
        while(x < len(IO)):
            if(time == ioOut[x]):
                Q.append(IO[x])
                print("time ", time, "ms: Process ", IO[x], " completed I/O; added to ready queue ",end = "", sep = "")
                ioOut.pop(x)
                IO.pop(x)
                printQueue(Q)
                cSwitches +=1
                x-=1
            x+=1


        if(len(processing) == 0 and len(toReady) == 0):
            if(len(Q) > 0 ):
                buffer -= 1
                if(buffer == contextSwitchTime/4 and len(buffQueue) == 0):
                    buffQueue.append(Q[0])
                    Q.pop(0)
            elif(len(buffQueue) == 1):
                buffer-=1
        
        
        
        if(len(toReady) == 1):
            readyBuff -=1
            if(readyBuff == 0):
                Q.append(toReady[0])
                toReady.pop(0)
        time += 1
    time += contextSwitchTime/2
    print("time ", int(time), "ms: Simulator ended for RR ", end = "", sep = "")
    printQueue(Q)


if __name__ == "__main__":
    test_Process = Processes(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]))
    test_Process.generateProcesses()
    test_Process.reorganizeData()
    RR(test_Process, int(sys.argv[5]), int(sys.argv[7]))