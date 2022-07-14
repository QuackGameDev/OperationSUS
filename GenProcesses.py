# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 21:50:17 2022

@author: Quang Nguyen
"""

from math import log
from math import ceil
from math import floor
import sys


class Rand48(object):
    
    def __init__(self, seed):
        self.n = seed
    
    def seed(self, seed):
        self.n = seed
    
    def srand(self, seed):
        self.n = (seed << 16) + 0x330e
    
    def next(self):
        self.n = (25214903917 * self.n + 11) & (2**48 - 1)
        return self.n
    
    def drand(self):
        return self.next() / 2**48
    
    def lrand(self):
        return self.next() >> 17
    
    def mrand(self):
        n = self.next() >> 16
        if n & (1 << 31):
            n -= 1 << 32
        return n


class Processes:   
    def __init__(self, numProcess, Seed, Lambda, upperBound):
        # argv[1]: num of processes
        self.num_process_ = numProcess
        
        # argv[2]: seed number
        self.seed_no_ = Seed
        
        # argv[3]: lambda
        self.lambda_ = Lambda
        
        # argv[4]: upper bound for random num gen (next_exp())
        self.upper_bound_ = upperBound
        
        # init guess for CPU burst time
        self.tau = int(1/self.lambda_)
        
        #specific seed for randomly generated number
        self.randSeed = Rand48(self.seed_no_)
        #seed declaration
        self.randSeed.srand(self.seed_no_)
        
        """ A dictionary with key: Process name and value: array of CPU and IO burst arrays
            layout:
            key: Process name
            value: [arrive time, tau, num burst, currentBurstIndex, [CPU Burst], [IO Burst]]
                num burst: Number of CPU and IO Burst
                currentBurstIndex: current burst that the Process is executing"""
        self.reorganizedData = {}
        
    # A testing method for puting info into a dict
    def reorganizeData(self):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
        for i in range(self.num_process_):
            info = []
            key = alphabet[i]
            info.append(self.arrival_Time[i])
            info.append(self.tau)
            info.append(self.num_Burst[i])
            
            currentBurstIndex = 0
            info.append(currentBurstIndex)
            
            info.append(self.CPU_Burst[i]) # a list
            info.append(self.IO_Burst[i]) # a list
        
        self.reorganizedData[key] = info

    # A testing method for puting info into a dict
    def printReorganizedData(self):
        #for evey key in processesDict
        for x in self.reorganizedData:
            info = "Key: {key} \t Value: {val}".format(key = x, val = self.reorganizedData.get(x))
            print(info)
    
    def next_exp(self):
        # generate numbers 
        ranNum = -log(self.randSeed.drand())/self.lambda_
        
        #re-gen number if exceed upper bound
        while(ranNum > self.upper_bound_):
            ranNum = -log(self.randSeed.drand())/self.lambda_
            
        return ranNum
    
        
    
    def generateProcesses(self):
        # 1D list
        """
        list of arrival time in alphabetical order
        A = > Z
        0 => 25 (index of the list)
        """
        self.arrival_Time = []
        self.num_Burst = []  # number of burst in a CPU
        
        # 2D List
        self.CPU_Burst = [[] for x in range(self.num_process_)]
        self.IO_Burst = [[] for x in range(self.num_process_)]
        
        
        for i in range(self.num_process_):
            self.arrival_Time.append(floor(self.next_exp()))
            self.num_Burst.append(ceil(self.randSeed.drand() * 100))
            
            for j in range(self.num_Burst[i] - 1):
                self.CPU_Burst[i].append(ceil(self.next_exp()))
                self.IO_Burst[i].append(ceil(self.next_exp()) * 10)
            self.CPU_Burst[i].append(ceil(self.next_exp()))
    
    
    
    def get_taus(self):
        # return a list of size "num_process_" in which all the entries are the initial tau value
        return [self.tau for i in range(self.num_process_)]
        
        
    def print(self):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
        for i in range(self.num_process_):
            if(self.num_Burst[i] < 2):
                info = "Process {process_Name}: arrival time {arriveTime}ms; tau {tau}ms; {numBurst} CPU burst:".format(process_Name = alphabet[i], 
                                                                                                                       arriveTime = self.arrival_Time[i], 
                                                                                                                       tau = self.tau, 
                                                                                                                       numBurst = self.num_Burst[i])
                print(info)
            else: 
                info = "Process {process_Name}: arrival time {arriveTime}ms; tau {tau}ms; {numBurst} CPU bursts:".format(process_Name = alphabet[i], 
                                                                                                                       arriveTime = self.arrival_Time[i], 
                                                                                                                       tau = self.tau, 
                                                                                                                       numBurst = self.num_Burst[i])
                print(info)
            
            for j in range(self.num_Burst[i] - 1):
                burst_Info = "--> CPU burst {CPUburst}ms --> I/O burst {IOburst}ms".format(CPUburst = self.CPU_Burst[i][j], IOburst = self.IO_Burst[i][j])
                print(burst_Info)
            lastCPU_Burst = "--> CPU burst {CPUburst}ms".format(CPUburst = self.CPU_Burst[i][-1])
            print(lastCPU_Burst)

        
        
if __name__ == "__main__":
    test_Process = Processes(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]))
    test_Process.generateProcesses()
    test_Process.print()