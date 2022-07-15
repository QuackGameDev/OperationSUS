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


if __name__ == "__main__":
    print("yeeet")
    test_Process = Processes(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]))
    test_Process.generateProcesses()
    test_Process.reorganizeData()
    test_Process.printReorganizedData()
    #test_Process.print()