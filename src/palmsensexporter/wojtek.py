import os
import time

from errno import EEXIST
from PalmSens import CurrentRange
from PalmSens import CurrentRanges
from PalmSens.Techniques import FastCyclicVoltammetry

import pspython.pspyfiles as pspyfiles
import pspython.pspyinstruments as pspyinstruments
import pspython.pspymethods as pspymethods



def new_data_callback(new_data):
    for type, value in new_data.items():
        print(type + ' = ' + str(value))
    return


def FastScanCyclicVoltammetry():
    FSCV = FastCyclicVoltammetry()

    FSCV.EquilibrationTime = 5
    FSCV.BeginPotential = -0.4
    FSCV.Vtx1Potential = 1.3
    FSCV.Vtx2Potential = -0.4
    FSCV.StepPotential = 0.0018
    FSCV.Scanrate = 400
    FSCV.nScans = 10
    FSCV.nAvgScans = 1 
    FSCV.nEqScans = 0
    FSCV.CellOnAfterMeasurement = False
    
    return FSCV

method = FastScanCyclicVoltammetry()

def get_current_range(id):
    """
    100 pA = 0,
    1 nA = 1,
    10 nA = 2,
    100 nA = 3,
    1 uA = 4,
    10 uA = 5,
    100 uA = 6,
    1 mA = 7,
    10 mA = 8,
    100 mA = 9,
    2 uA = 10,
    4 uA = 11,
    8 uA = 12,
    16 uA = 13,
    32 uA = 14,
    63 uA = 26,
    125 uA = 17,
    250 uA = 18,
    500 uA = 19,
    5 mA = 20,
    6 uA = 21,
    13 uA = 22,
    25 uA = 23,
    50 uA = 24,
    200 uA = 25
    """
    return CurrentRange(CurrentRanges(id)) 

method.Ranging.MaximumCurrentRange =  pspymethods.get_current_range(3)
method.Ranging.MinimumCurrentRange = pspymethods.get_current_range(3)
method.Ranging.StartCurrentRange = pspymethods.get_current_range(3)


if __name__ == '__main__':
    
    cwd = os.getcwd()

    try:
        os.makedirs(cwd + '/data')
    except OSError as exc:
        if exc.errno == EEXIST and os.path.isdir(cwd + '/data'):
            pass
        else: 
            raise

    start = time.time()  


    manager = pspyinstruments.InstrumentManager(new_data_callback=new_data_callback)
    available_instruments = pspyinstruments.discover_instruments()
    print('connecting to ' + available_instruments[0].name)
    success = manager.connect(available_instruments[0])

    if success == 1:

        print('connection established')

        measurement = manager.measure(method)

        if measurement is not None:
            print('measurement finished')
        else:
            print('failed to start measurement')

        success = manager.disconnect()

        pspyfiles.save_session_file(os.path.join(cwd, 'data') + '\save_test.pssession', [measurement])

        if success == 1:
            print('disconnected')
        else:
            print('error while disconnecting')

    else:
        print('connection failed')    
        
    end = time.time()

    print(f'The experimentwas split into  files in {end-start} seconds')