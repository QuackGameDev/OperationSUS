import sys
from math import log
from math import ceil
from math import floor

def outputStats(FCFS_stat, SJF_stat, SRT_stat, RR_stat):
    # open a (new) file to write
    outFile = open("simout.txt", "w")
    
    statDict = {"FCFS": FCFS_stat, 
                "SJF": SJF_stat, 
                "SRT": SRT_stat,
                "RR": RR_stat}
    
    for i in statDict:
        outFile.write("Algorithm {nameAlgo}\n".format(nameAlgo = i))
        outFile.write("-- average CPU burst time: {avgCPUtime} ms\n".format(avgCPUtime = ceil(statDict.get(i)[1] * 1000)/1000))
        outFile.write("-- average wait time: {avgWait} ms\n".format(avgWait = ceil(statDict.get(i)[2] * 1000)/1000))
        outFile.write("-- vaerage turnaround time: {avgTurn} ms\n".format(avgTurn = ceil(statDict.get(i)[3] * 1000)/1000))
        outFile.write("-- total number of context switches: {numSwitch}\n".format(numSwitch = statDict.get(i)[4]))
        outFile.write("-- total number of preemptions: {premept}\n".format(premept = statDict.get(i)[5]))
    
    
        # CPU utilization calculation
        outFile.write("-- CPU utilization: {CPUultil}%\n".format(CPUultil = statDict.get(i)[6]))
        
    outFile.close()