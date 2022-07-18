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
import sys
        
        
if __name__ == "__main__":
    #Error handling
    try:
        a = int(sys.argv[1])
        b = int(sys.argv[2])
        c = float(sys.argv[3])
        d = int(sys.argv[4])
        e = int(sys.argv[5])
        f = float(sys.argv[6])
        g = int(sys.argv[7])
    except ValueError:
        sys.stderr.write('Error: Invalid Argument!\n')
        sys.exit(2)
        
    # For printing the info of all processes
    test_Process = Processes(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]))
    test_Process.generateProcesses()
    contextSwitch = int(sys.argv[5])
    alpha = float(sys.argv[6])
    timeSlice = int(sys.argv[7])
    FCFS(test_Process, contextSwitch)
    SJF(test_Process, contextSwitch, alpha)
    SRT(test_Process, contextSwitch, alpha)
    RR(test_Process, contextSwitch, timeSlice)