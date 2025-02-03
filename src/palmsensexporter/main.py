'''
===================================================================================================
Copyright (C) 2024 Steven Linfield

This file is part of the palmsens-exporter package. This package is free software: you can 
redistribute it and/or modify it under the terms of the GNU General Public License as published by 
the Free Software Foundation, either version 3 of the License, or (at your option) any later 
version. This software is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
GNU General Public License for more details. You should have received a copy of the GNU General 
Public License along with palmsens-exporter. If not, see https://www.gnu.org/licenses/
===================================================================================================

Package title:      palmsens-exporter
Repository:         https://github.com/MoonshinetheP/palmsens-exporter
Date of creation:   11/10/2024
Main author:        Steven Linfield (MoonshinetheP)
Collaborators:      None
Acknowledgements:   None

Filename:           main.py

===================================================================================================

Description:

This file contains the code used by the palmsens-exporter package to .

===================================================================================================

How to use this file:
    


===================================================================================================
'''


import sys
import os
import clr
import time
from datetime import datetime

import numpy as np
import pandas as pd
import originpro as op
from originpro import pe as pe
from originpro import worksheet as ws

from tkinter import simpledialog, filedialog
from errno import EEXIST

import pspython.pspydata as psdata

# Load DLLs
scriptDir = os.path.dirname(os.path.realpath(__file__))
# This dll contains the classes in which the data is stored
clr.AddReference(scriptDir + '\\pspython' + '\\PalmSens.Core.dll')
# This dll is used to load your session file
clr.AddReference(scriptDir + '\\pspython' + '\\PalmSens.Core.Windows.dll')

# Import the static LoadSaveHelperFunctions
from System import Convert
from PalmSens.Windows import LoadSaveHelperFunctions
from PalmSens.Data import IDataValue
from PalmSens.Data import VoltageReading
from PalmSens.Data import CurrentReading


class ToOrigin:
    def __init__(self, input):
        
        # Input can be a list of .pssession files
        self.input = input

        # Functions and conditions set by originpro package
        def origin_shutdown_exception_hook(exctype, value, traceback):
            '''Ensures Origin gets shut down if an uncaught exception'''
            op.exit()
            sys.__excepthook__(exctype, value, traceback)

        if op and op.oext:
            sys.excepthook = origin_shutdown_exception_hook

        if op.oext:
            op.set_show(True)

        # Asks the user to enter a filename for the Origin file
        filename = simpledialog.askstring(title = 'Choose a filename', prompt = 'Enter your filename:', initialvalue = 'iNANO #xxx')
        
        # Opens a new Origin project
        op.new()

        # Loops through each of the .pssession files
        for ix in self.input:
                        
            session = LoadSaveHelperFunctions.LoadSessionFile(ix)
  
            file = os.path.split(ix)[1][:-10] 
            pe.cd('Folder1') # how to rename?
            pe.mkdir(file)
            pe.cd(file)

            # Loops through each measurement object in the .pssession file
            for iy in session:
                
                arrays = iy.DataSet.GetDataArrays()

                marker = datetime(iy.TimeStamp.Year, iy.TimeStamp.Month, iy.TimeStamp.Day, iy.TimeStamp.Hour, iy.TimeStamp.Minute, iy.TimeStamp.Second)

                wks = op.new_sheet('w', f'({marker.strftime('%Y-%m-%d - %X')}) - {iy.Title}')
                
                column = 0                                
                # Not sure how the index column is made in PSTrace, but this can be made here instead
                index = np.arange(1, arrays[0].Count + 1, 1).tolist()
                
                # Inserts the 'Index' string at the top of the array
                index.insert(0, 'Index')

                # Assigns the index column to the first column in the worksheet
                wks.from_list(column, index)
                
                values = {}
                for n in range(0, len(arrays)):
                    values.update({arrays[n].Description : []})

                # Loops through each array in the measurement object
                for iz in arrays:
                    
                    for n in range(0, iz.Count):

                        values[iz.Description].append(float(iz.get_Item(n).Value)) # need to know desription of current array

                        try:
                            extra = Convert.ChangeType(iz.get_Item(n), VoltageReading)
                            values[iz.Description].append(str(extra.Range.ToString())) # this won't work
                            values[iz.Description].append(str(extra.ReadingStatus.ToString()))                        
                        except: pass
                        
                        try:
                            extra = Convert.ChangeType(iz.get_Item(n), CurrentReading)
                            values[iz.Description].append(str(extra.CurrentRange.ToString()))
                            values[iz.Description].append(str(extra.ReadingStatus.ToString()))
                        except: pass



                    values.insert(0, f'{iz.Description}/{iz.Unit.ToString()}')
                    wks.from_list(column, values)

                    if iy.Method.ToString() == 'Electrochemical Impedance Spectroscopy':
                        pass
                    
                    if iy.Method.ToString() == 'Electrochemical Impedance Spectroscopy':    
                        pass  

                    if (psdata.ArrayType(iz.ArrayType) == psdata.ArrayType.Potential) or (psdata.ArrayType(iz.ArrayType) == psdata.ArrayType.Current):
                        try:
                            ranges.insert(0, f'{iz.Description}/{iz.Unit.ToString()}')
                            column += 1
                            wks.from_list(column, ranges)
                            status.insert(0, f'{iz.Description}/{iz.Unit.ToString()}')                        
                            column += 1
                            wks.from_list(column, status)
                        except: pass

        # Save the Origin project after 
        op.save(os.path.join(os.getcwd(), 'origin') + rf'\{filename}.opju')

        # Close the Origin project
        if op.oext:
            op.exit()


class ToText:
    def __init__(self):
        df = df.map(str)
        df_ns = df.copy()
        df_ns = df_ns.map(lambda x: x.replace(' ', ''))

        '''self.titles = []
        for ij in df.iloc[0]:
            if ij == 'nan' or ij[0:7] == 'Unnamed':
                pass
            else:
                self.titles.append(ij.replace("/",""))

        self.times = []        
        for ik in df.iloc[1]:
            if ik == 'nan' or ik[0:4] == 'Date':
                pass
            else:
                text = ik.replace(":", "-")
                text = text[:10] + ' -' +text[10:]
                self.times.append(text)
                
        self.index = []
        for il in range(0, df.shape[1]):
            if df.iloc[2][il] == 'index':
                self.index.append(il)
                
        last =[]
        for ix in df.iloc[2][self.index[-1]:]:
            last.append(str(ix))
        last = last.index('nan')

        
        for im in range(0, len(self.index)):
            try: 
                data = df_ns.iloc[2:, self.index[im]:self.index[im + 1]].dropna()
                data = data.to_string(header = False, index=False)

            except:
                data = df_ns.iloc[2:, self.index[im]:self.index[im] + last].dropna()
                data = data.to_string(header = False, index=False)

            with open(f'{cwd}/output/test', 'w', encoding="utf-16") as file:
                file.write(data)'''
        pass


if __name__ == "__main__":
    '''1. MAKE THE /DATA, /ANALYSIS, & /PLOTS FOLDERS''' 
    cwd = os.getcwd()

    try:
        os.makedirs(cwd + '/input')
    except OSError as exc:
        if exc.errno == EEXIST and os.path.isdir(cwd + '/input'):
            pass
        else: 
            raise

    try:
        os.makedirs(cwd + '/output')
    except OSError as exc:
        if exc.errno == EEXIST and os.path.isdir(cwd + '/output'):
            pass
        else: 
            raise

    start = time.time()  

    exported = ToOrigin(filedialog.askopenfilenames())

    end = time.time()
    print(f'The PalmSens file was split into  files in {end-start} seconds')