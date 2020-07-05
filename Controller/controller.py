# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 12:38:06 2020

@author: Manuel
"""



#---------
from tkinter import *
from tkinter.ttk import *


from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
#----------

import datetime
import time

import pandas as pd
import numpy as np

import nidaqmx




def startupdatGraph():
    updateGraph()
    if run == True:
        root.after(1000,startupdatGraph)
    
def updateGraph():
    global yIn, yOut, line1, canvas, ax
    

    # fig = mpl.figure.Figure(figsize=(5, 3))

    line1.set_data(np.arange(len(yIn)),np.array(yIn))
    ax.relim()
    ax.autoscale_view(True,True,True)
    
 
    canvas = FigureCanvasTkAgg(fig, root)
    canvas.get_tk_widget().grid(row=0, column=2)
    
    # fig_photo = draw_figure(canvas, fig)
    
def startController():
    global run, yIn, startTime
    print("Controller is running!")
    yIn=[]
    run = True
    startTime = datetime.datetime.now()
    startupdatGraph()
    runController()
    
def eval_timestamps():
    global timeList, startTime, stopTime
    
    
    stopTime = datetime.datetime.now()
    deltaT = stopTime - startTime
    deltaTms = deltaT.seconds*1000 + deltaT.microseconds/1000

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
    
    
def stopController():
    global run

    run = False
    updateGraph()
    
    eval_timestamps()    

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


root = Tk()
root.title("PID controller")

run = True

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


pPart = StringVar()
iPart = StringVar()
dPart = StringVar()

algorithmus = StringVar()


#ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
Label(mainframe, text="P-Part").grid(column=1, row=2, sticky=E) # ttk.Label()
Label(mainframe, text="I-Part").grid(column=1, row=3, sticky=E)
Label(mainframe, text="D-Part").grid(column=1, row=4, sticky=E)


pPart_entry = Entry(mainframe, width=7, textvariable=pPart) # ttk.Entry()
pPart_entry.grid(column=2, row=2, sticky=(W, E))

iPart_entry = Entry(mainframe, width=7, textvariable=iPart)
iPart_entry.grid(column=2, row=3, sticky=(W, E))

dPart_entry = Entry(mainframe, width=7, textvariable=dPart)
dPart_entry.grid(column=2, row=4, sticky=(W, E))


Button(mainframe, text="Start Control Loop", command=startController).grid(column=1, columnspan = 2,row=5, sticky=EW)
Button(mainframe, text="Stop", command=stopController).grid(column=1, columnspan = 2,row=6, sticky=EW)


for child in mainframe.winfo_children(): 
    child.grid_configure(padx=50, pady=5)

pPart_entry.focus()
root.bind('<Return>', startController)



# List to hold values
yIn = []
yOut = []

# Values/lists for evaluation the read/write frequency
startTime = 0
stopTime = 0
count = 0
timeList = []


# Generate some start/example data
X = 0
Y = 0
# Setup the graph
fig = Figure(figsize=(5, 3), dpi=100)
ax = fig.add_subplot(1, 1, 1)
line1, = ax.plot(X, Y)
plt.title("Input Data")
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().grid(row=0, column=2)

with nidaqmx.Task() as inputTask,nidaqmx.Task() as outputTask:
    device = "Dev2"
    inputTask.ai_channels.add_ai_voltage_chan(device + "/ai0")
    outputTask.ao_channels.add_ao_voltage_chan(device + "/ao0",min_val=0,max_val=5)
    inputTask.start()
    outputTask.start()
    root.mainloop()

    