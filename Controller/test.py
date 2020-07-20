# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 23:29:56 2020

@author: Manuel
"""


import nidaqmx



with nidaqmx.Task() as inputTask,nidaqmx.Task() as outputTask:
    device = "Dev1"
    inputTask.ai_channels.add_ai_voltage_chan(device + "/ai0")
    outputTask.ao_channels.add_ao_voltage_chan(device + "/ao0",min_val = 0,max_val = 5) # bei usb 6001 max_val = 10


    inputTask.start()
    outputTask.start()
    
    while True:
        inpu = inputTask.read()
        print(inpu)
        outputTask.write(inpu)