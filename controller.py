# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 12:38:06 2020

@author: Manuel
"""
from tkinter import *
from tkinter import ttk 
from random import random
import datetime
import time
import pandas as pd

import nidaqmx

import csv # for dummy read/write
import os # for dummy read/write

import numpy as np

import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg
#import matplotlib.pyplot as plt
import matplotlib as mpl


def startupdatGraph():
    updateGraph()
    if run == True:
        root.after(1000,startupdatGraph)
    
def updateGraph():
    global yIn, yOut, canvas,fig_photo
    fig = mpl.figure.Figure(figsize=(5, 3))
    ax = fig.add_subplot(111)
    ax.plot(np.array(yIn))
    ax.set_xlim([0,10000])
    fig_photo = draw_figure(canvas, fig)
    
def startController():
    global run, yIn, startTime
    yIn=[]
    run = True
    startTime = datetime.datetime.now()
    startupdatGraph()
    runController()
    
def stopController():
    global run, count, startTime, stopTime, timeList
    
    
    df_timeList = pd.DataFrame(timeList)
    
    
    
    stopTime = datetime.datetime.now()
    deltaT = stopTime - startTime
    deltaTms = deltaT.seconds*1000 + deltaT.microseconds/1000

    print("Count = " + str(count))
    print("deltaT in ms: " + str(deltaTms))
    print("Time per cycle [ms]: " + str(deltaTms/count))
 
    count = 0
    run = False
    updateGraph()
    
def readInput():
    return random()
    
def writeOutput(output):
    with open('output.csv', 'w') as output_file:
        outputTask = csv.writer(output_file)
        outputTask.writerow([output])

def runController(*args):
    if run == True:
        cycleTime = 1 # in ms   
        root.after(cycleTime,runController)
        
        global inputTask, outputTask, yIn, yOut, count, timeList
        count=count+1
#        t = datetime.datetime.now()
#        timeList.append(t.second + t.microsecond*1e6)
        df_timeList["dt"]
        inp = inputTask.read()
#        inp = readInput() #dummy: read from csv or random

        output = calcOutputAlg1(inp)
        yIn.append(inp)
        yOut.append(output)
                    
        outputTask.write(output)
#        writeOutput(output) # dummy: write to csv

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

def draw_figure(canvas, figure, loc=(0, 0)):
    """ Draw a matplotlib figure onto a Tk canvas

    loc: location of top-left corner of figure on canvas in pixels.
    Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
    """
    figure_canvas_agg = FigureCanvasAgg(figure)
    figure_canvas_agg.draw()
    figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
    figure_w, figure_h = int(figure_w), int(figure_h)
    photo = PhotoImage(master=canvas, width=figure_w, height=figure_h)

    # Position: convert from top-left anchor to center anchor
    canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)

    # Unfortunately, there's no accessor for the pointer to the native renderer
    tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

    # Return a handle which contains a reference to the photo object
    # which must be kept live or else the picture disappears
    return photo

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
ttk.Label(mainframe, text="P-Part").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="I-Part").grid(column=1, row=3, sticky=E)
ttk.Label(mainframe, text="D-Part").grid(column=1, row=4, sticky=E)


pPart_entry = ttk.Entry(mainframe, width=7, textvariable=pPart)
pPart_entry.grid(column=2, row=2, sticky=(W, E))

iPart_entry = ttk.Entry(mainframe, width=7, textvariable=iPart)
iPart_entry.grid(column=2, row=3, sticky=(W, E))

dPart_entry = ttk.Entry(mainframe, width=7, textvariable=dPart)
dPart_entry.grid(column=2, row=4, sticky=(W, E))


ttk.Button(mainframe, text="Start Control Loop", command=startController).grid(column=1, columnspan = 2,row=5, sticky=EW)
ttk.Button(mainframe, text="Stop", command=stopController).grid(column=1, columnspan = 2,row=6, sticky=EW)


for child in mainframe.winfo_children(): child.grid_configure(padx=50, pady=5)

pPart_entry.focus()
root.bind('<Return>', startController)


w, h = 500, 300
canvas = Canvas(root, width=w, height=h)
canvas.grid(column=3, row=0,rowspan=5,sticky=NS)

# Generate some example data
X = 0
Y = 0
yIn = []
yOut = []

startTime = 0
stopTime = 0
count = 0
timeList = []
# Create the figure we desire to add to an existing canvas
fig = mpl.figure.Figure(figsize=(5, 3))
ax = fig.add_subplot(111)
ax.set_xlim([0,10000])
#ax.plot(X,Y)

# Keep this handle alive, or else figure will disappear
fig_photo = draw_figure(canvas, fig)

# remove csv-file before writing again
try:
    os.remove('output.csv')
except:
    print("No output.csv availible")
with nidaqmx.Task() as inputTask,nidaqmx.Task() as outputTask:
    device = "Dev1"
    inputTask.ai_channels.add_ai_voltage_chan(device + "/ai0")
    outputTask.ao_channels.add_ao_voltage_chan(device + "/ao0",min_val=0,max_val=5)
    inputTask.start()
    outputTask.start()
    root.mainloop()

    