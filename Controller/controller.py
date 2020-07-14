# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 12:38:06 2020

@author: Manuel
"""



#---------
import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import matplotlib.pyplot as plt

import time

import pandas as pd
import numpy as np

import nidaqmx
#----------



def updateGraph():
    global yIn, yOut, line1, canvas, ax, fig
    
    line1.set_data(np.arange(len(yIn)),np.array(yIn))
    ax.relim()
    ax.autoscale_view(True,True,True)
    
 
    canvas = FigureCanvasTkAgg(fig, root)
    canvas.get_tk_widget().grid(row = 0, column = 2)
    
def startupdatGraph():
    updateGraph()
    if run == True:
        root.after(1000,startupdatGraph)

def check_DI_2start():
    print(digitalInputTask.read())

def activateController():
    global run, yIn, yOut, timeList, startTime
    run = True
    timeList = []
    count = 0
    yIn = []
    yOut = []
    print("Controller is active!")
    while not digitalInputTask.read():
        print(digitalInputTask.read())
        print(digitalInputTask.read())
        time.sleep(2e-3)
        
        if not run:
            break

###### maybe a startController func is needed and remove the while-loop to not block th ui. instead a root.after is needed maybe


        
        
    if run:
        print("Controller is running!")
  
        startTime = time.time()
        startupdatGraph()
        runController()
    
def eval_timestamps():
    global timeList, startTime, stopTime, count
    
    
    stopTime = time.time()
    deltaT = stopTime - startTime
    deltaTms = deltaT*1e3

    print("Count = " + str(count))
    print("deltaT in ms: " + str(deltaTms))
    print("Time per cycle [ms]: " + str(deltaTms/count))
    df_timeList = pd.DataFrame(timeList)
    df_timeList.columns = ['Time_ns']
    df_timeList["dt_ns"] = df_timeList.Time_ns.diff().fillna(0).astype(int)
    df_timeList["Time_ms"] = df_timeList["Time_ns"]/1e6
    df_timeList["Time_ms"] = df_timeList["Time_ms"].astype("int64")
    
    df_timeList["dt_ms"] = df_timeList.Time_ms.diff().fillna(0).astype(int)
    
    df_timeList["dt_ms"].hist()
    
    print(df_timeList.dtypes)


def logValues2csv():
    global timeList, yIn, yOut
    

    print(len(timeList))
    print(len(yIn))
    print(len(yOut))
    
    
    df = pd.DataFrame(
    {'Time': timeList,
      'yIn': yIn,
      'yOut': yOut
      })
    
    df.to_csv("valueLogs\\vals.csv",index=False,sep=";")
    
def stopController():
    global run, logVals

    run = False
    updateGraph()
    
    eval_timestamps()  
    if logVals:
        logValues2csv()

def runController(*args):
    if run == True:
        cycleTime = 1 # in ms   
        root.after(cycleTime,runController)
        
        global inputTask, outputTask, yIn, yOut, count, timeList
        count=count+1
        time.time_ns()
        timeList.append(time.time_ns())

        inp = inputTask.read()

        output = calcOutputAlg1(inp)
        yIn.append(inp)
        yOut.append(output)
                    
        outputTask.write(output)

def calcOutputAlg1(inp):
#    P = pPart.get()
#    I = iPart.get()
#    D = dPart.get()
    output = inp/5
    return output**2

def calcOutputAlg2(inp):
    output = inp+2
    return output

def calcOutputAlg3(inp):
    output = inp+3
    return output



root = tk.Tk()
root.title("PID controller")

run = True

mainframe = tk.Frame(root)#, padding="3 3 12 12") 
mainframe.grid(column = 0, row=0, sticky = (tk.N, tk.W, tk.E, tk.S))
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)


pPart = tk.StringVar()
iPart = tk.StringVar()
dPart = tk.StringVar()
setPoint = tk.StringVar()

algorithmus = tk.StringVar()


#ttk.Label(mainframe, text = "feet").grid(column = 3, row = 1, sticky = tk.W)
tk.Label(mainframe, text = "P-Part").grid(column = 1, row = 2, sticky = tk.E)
tk.Label(mainframe, text = "I-Part").grid(column = 1, row = 3, sticky = tk.E)
tk.Label(mainframe, text = "D-Part").grid(column = 1, row = 4, sticky = tk.E)
tk.Label(mainframe, text = "Set Point").grid(column = 1, row = 5, sticky = tk.E)

pPart_entry = tk.Entry(mainframe, width = 7, textvariable = pPart) # ttk.Entry()
pPart_entry.grid(column = 2, row = 2, sticky = (tk.W, tk.E))

iPart_entry = tk.Entry(mainframe, width = 7, textvariable = iPart)
iPart_entry.grid(column = 2, row = 3, sticky = (tk.W, tk.E))

dPart_entry = tk.Entry(mainframe, width=7, textvariable=dPart)
dPart_entry.grid(column = 2, row = 4, sticky = (tk.W, tk.E))

setPoint_entry = tk.Entry(mainframe, width = 7, textvariable = setPoint)
setPoint_entry.grid(column = 2, row = 5, sticky = (tk.W, tk.E))

tk.Button(mainframe, text = "Start Control Loop", command = activateController).grid(column = 1, columnspan = 2,row = 5, sticky = tk.EW)
tk.Button(mainframe, text = "Stop", command = stopController).grid(column = 1, columnspan = 2,row = 6, sticky = tk.EW)


for child in mainframe.winfo_children(): 
    child.grid_configure(padx = 50, pady = 5)

pPart_entry.focus()
root.bind('<Return>', activateController)



# List to hold values
yIn = []
yOut = []

# Values/lists for evaluation the read/write frequency
startTime = 0
stopTime = 0
count = 0
timeList = []
logVals = True

# Generate some start/example data
X = 0
Y = 0
# Setup the graph
fig = Figure(figsize = (5, 3), dpi = 100)
ax = fig.add_subplot(1, 1, 1)
line1, = ax.plot(X, Y)
ax.set_title("Input Signal")
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().grid(row = 0, column = 2)

with nidaqmx.Task() as inputTask,nidaqmx.Task() as outputTask, nidaqmx.Task() as digitalInputTask:
    device = "Dev2"
    digitalInputTask.di_channels.add_di_chan(device + "/port0/line0")
    inputTask.ai_channels.add_ai_voltage_chan(device + "/ai0")
    outputTask.ao_channels.add_ao_voltage_chan(device + "/ao0",min_val = 0,max_val = 5) # bei usb 6001 max_val = 10
    inputTask.start()
    outputTask.start()
    root.mainloop()

    