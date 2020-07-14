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

class myApp(tk.Tk):
    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)
        
        
        self.pPart = LabelParameterPair("P-part",1)
        self.iPart = LabelParameterPair("I-part",2)
        self.dPart = LabelParameterPair("D-part",3)
        self.setPoint = LabelParameterPair("Set Point",4)
   
        
        tk.Button(text = "Start Control Loop", command = self.activateController).grid(column = 1, columnspan = 2,row = 6, sticky = tk.EW)
        tk.Button( text = "Stop Control Loop", command = self.stopController).grid(column = 1, columnspan = 2,row = 7, sticky = tk.EW)


    def activateController(*args):
        print("In activateController")

        
    def stopController(*args):
        print("In stopController")

class LabelParameterPair():
    def __init__(self,_name,row,*args,**kwargs):
        self._value = tk.StringVar()
        self._label = tk.Label( text = _name).grid(column = 1, row = row, sticky = tk.E, padx=15, pady=15)
        self._entry = tk.Entry( width = 7, textvariable = self._value).grid(column = 2, row = row, sticky = (tk.W, tk.E))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        