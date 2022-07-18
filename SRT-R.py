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
    # This sorts the Queue by tau and if that fails, by alphabet
    def sortQueue(e):
        return processesInfo.get(e).get("tau"),ord(e)

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

    preempting=[]
    preempt = False
    # For the recalculation of tau after completeing a CPU Burst
    old_tau =0

    # Alpha that is given by the user
    alpha = 0.75
    # The transfer between IO to ready queue, holds the time in which they re enter.
    IO_to_ready = []
    printcorrectly = False
    print("time 0ms: Simulator started for SJF [Q: empty]")
    timer  = 0
    while(not allProcessTerminate):
        # if there are still Processes left to arrive, print that out
        processesNameList = allIndexOfTargerNum(timer, arrivalTimer)
        if(numProcess > 0 and len(processesNameList) > 0):
            # add all of the processes to the queue
            for i in processesNameList:
                ready_queue.append(alphabet[i])
                ready_queue.sort(key=sortQueue)
                print("time "+str(timer)+"ms: Process "+str(alphabet[i])+" (tau "+str(processesInfo.get(alphabet[i]).get("tau"))+"ms) arrived; added to ready queue "+print_ready_queue(ready_queue))
        # This activates only if IO queue has any processes inside.

                # When the CPU Burst is done
        if CPUburst ==True and timer_for_CPU_burst==0:
            #print("CPU Burst complete: "+str(timer))
            if (len(processesInfo.get(CPUqueue[0]).get("CPUBurst"))-processesInfo.get(CPUqueue[0]).get("currentBurstIndex")-1)==0:
                print("time "+str(timer)+"ms: Process "+str(CPUqueue[0])+" terminated "+print_ready_queue(ready_queue))
                completed.append(CPUqueue[0])
                #print(completed)
                #print(numProcess)
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
                #print(CPUqueue[0],timer)
                old_tau = processesInfo.get(CPUqueue[0]).get("tau")
                processesInfo.get(CPUqueue[0])["tau"]= math.ceil(alpha * actual_burst +(1-alpha) * old_tau)
                print("time "+str(timer)+"ms: Recalculated tau for process "+str(CPUqueue[0])+": old tau "+str(old_tau)+"ms; new tau "+str(processesInfo.get(CPUqueue[0]).get("tau"))+"ms "+print_ready_queue(ready_queue))
                print("time "+str(timer)+"ms: Process "+str(CPUqueue[0])+" switching out of CPU; will block on I/O until time "+str(timer+processesInfo.get(CPUqueue[0]).get("IOBurst")[processesInfo.get(CPUqueue[0]).get("currentBurstIndex")]+contextSwitch)+"ms "+print_ready_queue(ready_queue))
                CPUqueue.pop(0)
                timer_for_switch=contextSwitch
                CPUburst = False

        if(len(IOqueue)>0):
            i=0
            # This checks all inside the IO queue if any have reached their destination. If it does
            # , the process is removed from the IO queue and goes into standby IO_to_ready
            while i < len(IOqueue):
                if(processesInfo.get(IOqueue[i]).get("IOBurst")[processesInfo.get(IOqueue[i]).get("currentBurstIndex")]==0):
                    IO_to_ready.append((IOqueue[i],timer+contextSwitch))
                    IOqueue.remove(IOqueue[i])
                    i-=1
                i+=1

        if CPUburst == True and timer_for_switch==0 and len(preempting)>0:
            print("time "+str(timer)+"ms: Process "+str(preempting[0][0])+" (tau "+str(processesInfo.get(CPUqueue[0]).get("tau"))+"ms) started using the CPU for remaining "+str(preempting[0][1])+"ms of "+str(preempting[0][2])+" burst "+print_ready_queue(ready_queue))
            timer_for_CPU_burst = preempting[0][1]
            actual_burst =preempting[0][2]
            preempting.pop(0)
            #print("CPU Burst start: "+str(timer)+" Process : "+str(CPUqueue[0]) +" Burst timer: "+str(actual_burst))      

        if CPUburst == True and timer_for_switch==0 and len(preempting)==0:
            print("time "+str(timer)+"ms: Process "+str(CPUqueue[0])+" (tau "+str(processesInfo.get(CPUqueue[0]).get("tau"))+"ms) started using the CPU for "+str(processesInfo.get(CPUqueue[0]).get("CPUBurst")[processesInfo.get(CPUqueue[0]).get("currentBurstIndex")])+"ms burst "+print_ready_queue(ready_queue))
            timer_for_CPU_burst = processesInfo.get(CPUqueue[0]).get("CPUBurst")[processesInfo.get(CPUqueue[0]).get("currentBurstIndex")]
            actual_burst =timer_for_CPU_burst
            #print("CPU Burst start: "+str(timer)+" Process : "+str(CPUqueue[0]) +" Burst timer: "+str(actual_burst))      


        # This activates only if there are processes just waiting to head into ready queue from IO queue
        if(len(IO_to_ready)>0):
            i=0
            IO_to_ready.sort()
            while i <(len(IO_to_ready)):
                if(IO_to_ready[i][1]==timer):
                    processesInfo.get(IO_to_ready[i][0])["currentBurstIndex"]+=1
                    # Prempting
                    if( processesInfo.get(IO_to_ready[i][0])["tau"] < processesInfo.get(CPUqueue[0])["tau"] and timer_for_CPU_burst > processesInfo.get(IO_to_ready[i][0]).get("CPUBurst")[processesInfo.get(CPUqueue[0])["currentBurstIndex"]] ):
                        ready_queue.append(IO_to_ready[i][0])
                        ready_queue.sort(key=sortQueue)
                        print("time "+str(timer)+"ms: Process "+IO_to_ready[i][0]+" (tau "+str(processesInfo.get(IO_to_ready[i][0]).get("tau"))+"ms) completed I/O; preempting "+CPUqueue[0]+" "+print_ready_queue(ready_queue))
                        preempting.append([CPUqueue[0],timer_for_CPU_burst,processesInfo.get(CPUqueue[0]).get("CPUBurst")[processesInfo.get(CPUqueue[0])["currentBurstIndex"]]] )
                        timer_for_switch=contextSwitch
                        CPUqueue.append(ready_queue[0])
                        ready_queue.pop(0)
                        preempt = True
                    else:
                        ready_queue.append(IO_to_ready[i][0])
                        ready_queue.sort(key=sortQueue)
                        print("time "+str(timer)+"ms: Process "+IO_to_ready[i][0]+" (tau "+str(processesInfo.get(IO_to_ready[i][0]).get("tau"))+"ms) completed I/O; added to ready queue "+print_ready_queue(ready_queue))
                        
                    IO_to_ready.pop(i)
                    if(CPUburst == False and len(ready_queue)>0 and timer_for_switch<=0):
                        printcorrectly = True
                    i-=1
                i+=1
            if(printcorrectly == True):
                ready_queue.sort(key=sortQueue)
                CPUqueue.append(ready_queue[0])
                CPUburst = True
                timer_for_switch=contextSwitch
                ready_queue.pop(0)
                printcorrectly = False


        if( CPUburst == False and len(preempting)>0 and timer_for_switch<=0 and preempt == True):
            CPUqueue.append(preempting[0][0])
         
            CPUburst = True
            timer_for_switch=contextSwitch

        #This makes sure that the CPU burst always only has one process inside and not being occupied by the context switch
        if( CPUburst == False and len(ready_queue)>0 and timer_for_switch<=0):
            CPUqueue.append(ready_queue[0])
            ready_queue.pop(0)
            CPUburst = True
            timer_for_switch=contextSwitch
            preempt == False
        # After getting the content switch done after moving in a new process, CPU Burst is set up and the CPU timer ticks from now on

            

        if(len(completed)==numProcess or timer_for_switch<-10000000000):
            timer+=contextSwitch 
            print("time "+str(timer)+"ms: Simulator ended for SJF "+print_ready_queue(ready_queue))
            allProcessTerminate=True

        if len(IOqueue)>0:
            for i in IOqueue:
                processesInfo.get(i).get("IOBurst")[processesInfo.get(i).get("currentBurstIndex")]-=1
        #print("CPU Burst timer:"+str(timer_for_CPU_burst) +" Timer: "+str(timer) + " how long: = " +str(timer +timer_for_CPU_burst))
        timer_for_CPU_burst-=1
        timer_for_switch -=1
        timer += 1

if __name__ == "__main__":
    test_Process = Processes(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]))
    test_Process.generateProcesses()
    test_Process.reorganizeData()
    SJF(test_Process,4)
    