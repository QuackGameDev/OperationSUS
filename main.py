# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 21:50:17 2022

@author: Quang Nguyen, Roger Luo, Raph Chung
"""

from GenProcesses import *
from FCFS import *
from SJF import *
from SRT import *
from RR import *
        
        
if __name__ == "__main__":
    # For printing the info of all processes
    test_Process = Processes(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]))
    test_Process.generateProcesses()
    test_Process.print()
    contextSwitch = int(sys.argv[5])
    alpha = float(sys.argv[6])
    timeslice = int(sys.argv[7])
    #FCFS(test_Process, contextSwitch)
    #SJF() Add the parameters, I dunno what they are
    #SRT(test_Process, contextSwitch, alpha)
    #RR(test_Process, contextSwitch, timeslice)