# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 22:52:21 2020

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

class MyApp(tk.Tk):
    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)
        
        self.controller = Controller(self)
        
        
        self.pPart = LabelParameterPair("P-part",1)
        self.iPart = LabelParameterPair("I-part",2)
        self.dPart = LabelParameterPair("D-part",3)
        self.setPoint = LabelParameterPair("Set Point",4)
        
        
        tk.Button(text = "Start Control Loop", command = self.controller.activateController).grid(column = 1, columnspan = 2,row = 6, sticky = tk.EW)
        tk.Button( text = "Stop Control Loop", command = self.controller.stopController).grid(column = 1, columnspan = 2,row = 7, sticky = tk.EW)

 

    # def activateController(self):
    #     print("In activateController")
    #     print("pPart = {}".format(self.pPart._value.get()))

        
    # def stopController(*args):
    #     print("In stopController")


class Controller():
    def __init__(self,app):

        self.run = False
        self.app = app
        
        

        

    def runController(self):
        print("In runController------------------")
        # global inputTask
        print("self" + str(self))
        print("inputTask = "  )
        print(self.inputTask)
        cycleTime = 100 # in ms   

            
        if self.run:
            print("---")
            print(self.runController)
            self.app.after(cycleTime,self.runController)
            print("val = {}".format(self.inputTask.read()))
        # while self.run:
        #     print(inputTask.read())
        #     time.sleep(2e-3)            
            
            
            
            
    def activateController(self):
        print("In activateController")
        self.run = True
        
        with nidaqmx.Task() as self.inputTask,nidaqmx.Task() as self.outputTask:
            device = "Dev1"
            self.inputTask.ai_channels.add_ai_voltage_chan(device + "/ai0")
            self.outputTask.ao_channels.add_ao_voltage_chan(device + "/ao0",min_val = 0,max_val = 5) # bei usb 6001 max_val = 10
            self.inputTask.start()
            self.outputTask.start()
            
            print(self.inputTask)
            print(self.runController)
            print("----------")
            self.runController()



        
    def stopController(self):
        print("In stopController")
        self.run = False

class LabelParameterPair():
    def __init__(self,_name,row,*args,**kwargs):
        self._value = tk.StringVar()
        self._label = tk.Label( text = _name).grid(column = 1, row = row, sticky = tk.E, padx=15, pady=15)
        self._entry = tk.Entry( width = 7, textvariable = self._value).grid(column = 2, row = row, sticky = (tk.W, tk.E))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        