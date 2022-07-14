# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 21:59:20 2022

@author: Quang Nguyen
"""
# parameter: pass in a Processes class
def RR(processes, contextSwitchTime, timeSlice):
    queue = []
    processing = []
    completed = []
    allCompleted = False # keep track of when all of the processes is completed or not
    print("time 0ms: Simulator started for RR with time slice {ts}ms [Q: empty]".format(ts = timeSlice))
    timer = 0