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
import math
def allIndexOfTargerNum(targetNum, list):
    allIndex = []
    for i in range(len(list)):
        if (targetNum == list[i]):
            allIndex.append(i)
            
    return allIndex

def sortQueue(Processes):
    newQueue = []

def print_ready_queue(ready_queue):
    if(len(ready_queue)==0):
        info="[Q: empty]"
        return info
    else:
        info="[Q: "
        for i in ready_queue:
            info+=i
            info+=" "
        info = info.rstrip(info[-1])
        info.strip(" ")
        info+="]"
        return info
    

def SJF(Processes, contextSwitchTime):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # tell whenever the algo is done so the timer stop
    allProcessTerminate = False
    
    # In charge of how many processes
    numProcess = Processes.num_process_ 

    # a LIST that keep track of the time that the next process arrive. Pop arrival_Time[0] out once timer = arrival_Time[0]
    arrivalTimer = Processes.arrival_Time
    
    # a dict of all of the info of all processes
    processesInfo = Processes.reorganizedData
    

    # list of processes in the ready queue
    ready_queue = []
    
    # list of processes in the IO Burst State
    IOqueue = []
    
    # list of processes in the CPU Burst State
    CPUqueue = []
    
    # list of processes finish both IO and CPU Burst
    completed = []

    CPUburst = False

    contextSwitch =2

    timer_for_switch=-1

    timer_for_CPU_burst=-1

    actual_burst=-1
    old_tau =0
    alpha = 0.5
    
    print("time 0ms: Simulator started for SJF [Q: empty]")
    timer  = 0
    while(not allProcessTerminate):
        # if there are still Processes left to arrive, print that out
        processesNameList = allIndexOfTargerNum(timer, arrivalTimer)
        if(numProcess > 0 and len(processesNameList) > 0):
            # add all of the processes to the queue
            for i in processesNameList:
                ready_queue.append(alphabet[i])
                print("time "+str(timer)+"ms: Process "+str(alphabet[i])+" (tau "+str(processesInfo.get(alphabet[i]).get("tau"))+"ms) arrived; added to ready queue "+print_ready_queue(ready_queue))
                # print(ready_queue)
                # print(len(ready_queue))
        if(len(IOqueue)>0):
            for i in IOqueue:
                if(processesInfo.get(i).get("IOBurst")[processesInfo.get(i).get("currentBurstIndex")]==0):
                    ready_queue.append(i)
                    timer+=2
                    print("time "+str(timer)+"ms: Process "+i+" (tau "+str(processesInfo.get(i).get("tau"))+"ms) completed I/O; added to ready queue "+print_ready_queue(ready_queue))
                    processesInfo.get(i)["currentBurstIndex"]+=1
                    IOqueue.remove(i)
                    for i in IOqueue:
                        processesInfo.get(i).get("IOBurst")[processesInfo.get(i).get("currentBurstIndex")]-=2

       
        if( CPUburst == False and len(ready_queue)>0 and timer_for_switch<=0):
            CPUqueue.append(ready_queue[0])
            ready_queue.pop(0)
            CPUburst = True
            timer_for_switch=contextSwitch
            
        if CPUburst == True and timer_for_switch==0:
            print("time "+str(timer)+"ms: Process "+str(CPUqueue[0])+" (tau "+str(processesInfo.get(CPUqueue[0]).get("tau"))+"ms) started using the CPU for "+str(processesInfo.get(CPUqueue[0]).get("CPUBurst")[processesInfo.get(CPUqueue[0]).get("currentBurstIndex")])+"ms burst "+print_ready_queue(ready_queue))
            timer_for_CPU_burst = processesInfo.get(CPUqueue[0]).get("CPUBurst")[processesInfo.get(CPUqueue[0]).get("currentBurstIndex")]
            actual_burst =timer_for_CPU_burst
            

        if CPUburst ==True and timer_for_CPU_burst==0:
            if (len(processesInfo.get(CPUqueue[0]).get("CPUBurst"))-processesInfo.get(CPUqueue[0]).get("currentBurstIndex")-1)==0:
                print("time "+str(timer)+"ms: Process "+str(CPUqueue[0])+" terminated "+print_ready_queue(ready_queue))
                completed.append(CPUqueue[0])
                CPUqueue.pop(0)
                timer_for_switch=contextSwitch
                CPUburst = False
            #Time to put into I/O Burst and end the CPU Burst
            else:
                if(len(processesInfo.get(CPUqueue[0]).get("CPUBurst"))-processesInfo.get(CPUqueue[0]).get("currentBurstIndex")-1)==1:
                    print("time "+str(timer)+"ms: Process "+str(CPUqueue[0])+" (tau "+str(processesInfo.get(CPUqueue[0]).get("tau"))+"ms) completed a CPU burst; "+str(len(processesInfo.get(CPUqueue[0]).get("CPUBurst"))-processesInfo.get(CPUqueue[0]).get("currentBurstIndex")-1)+" burst to go "+print_ready_queue(ready_queue))
                else:
                    print("time "+str(timer)+"ms: Process "+str(CPUqueue[0])+" (tau "+str(processesInfo.get(CPUqueue[0]).get("tau"))+"ms) completed a CPU burst; "+str(len(processesInfo.get(CPUqueue[0]).get("CPUBurst"))-processesInfo.get(CPUqueue[0]).get("currentBurstIndex")-1)+" bursts to go "+print_ready_queue(ready_queue))
                IOqueue.append(CPUqueue[0])
                old_tau = processesInfo.get(CPUqueue[0]).get("tau")
                processesInfo.get(CPUqueue[0])["tau"]= math.ceil(alpha * actual_burst +(1-alpha) * old_tau)
                print("time "+str(timer)+"ms: Recalculated tau for process "+str(CPUqueue[0])+": old tau "+str(old_tau)+"ms; new tau "+str(processesInfo.get(CPUqueue[0]).get("tau"))+"ms "+print_ready_queue(ready_queue))
                print("time "+str(timer)+"ms: Process "+str(CPUqueue[0])+" switching out of CPU; will block on I/O until time "+str(timer+processesInfo.get(CPUqueue[0]).get("IOBurst")[processesInfo.get(CPUqueue[0]).get("currentBurstIndex")]+2)+"ms "+print_ready_queue(ready_queue))

                CPUqueue.pop(0)
                timer_for_switch=contextSwitch
                CPUburst = False

        if(len(completed)==numProcess):
            timer+=2
            print("time "+str(timer)+"ms: Simulator ended for SJF "+print_ready_queue(ready_queue))
            allProcessTerminate=True
        #all the minussy stuff

        if len(IOqueue)>0:
            for i in IOqueue:
                processesInfo.get(i).get("IOBurst")[processesInfo.get(i).get("currentBurstIndex")]-=1
                
        timer_for_CPU_burst-=1
        timer_for_switch -=1
        timer += 1

if __name__ == "__main__":
    test_Process = Processes(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]))
    test_Process.generateProcesses()
    test_Process.reorganizeData()
    test_Process.printReorganizedData()
    #test_Process.print()
    # for i in test_Process.reorganizedData:
    #         #print(test_Process.reorganizedData.get(i).get("arrivalTime"))
    #         test_Process.reorganizedData.get(i)["arrivalTime"]=4
    #         print(test_Process.reorganizedData.get(i).get("CPUBurst")[test_Process.reorganizedData.get(i).get("currentBurstIndex")])
    #         print(test_Process.reorganizedData.get(i).get("IOBurst")[test_Process.reorganizedData.get(i).get("currentBurstIndex")])
    #         info = "Key: {key}\n".format(key = i) 
    #         info += "Value: \n\t"
    #         for j in test_Process.reorganizedData.get(i):
    #             info += "Key: {keyInner}; Value: {valInner}\n\t".format(keyInner = j, valInner = test_Process.reorganizedData.get(i).get(j))
    #         print(info)
    SJF(test_Process,4)
    