import pspython.pspyinstruments as pspyinstruments
import pspython.pspyfiles as pspyfiles
import pspython.pspymethods as pspymethods
import os

from PalmSens.Techniques import MethodScriptSandbox

def new_data_callback(new_data):
    for type, value in new_data.items():
        print(type + ' = ' + str(value))
    return

#scriptDir = os.path.dirname(os.path.realpath(__file__))

manager = pspyinstruments.InstrumentManager(new_data_callback=new_data_callback)

available_instruments = pspyinstruments.discover_instruments()
print('connecting to ' + available_instruments[0].name)
success = manager.connect(available_instruments[0])

method = MethodScriptSandbox()
script = '''e
var y
var w # temporary variable
var i # array index current scan
var j # array index total scan
var k # scan index
array e 81i # array with potentials
array l 81i # array with currents
# 25000 - 81 / 81 = approximately 300 scans
# 300 * 81
array m 24300i # array with all potentials
array n 24300i # array with all currents
set_pgstat_chan 0
set_pgstat_mode 3
# set filters
set_acquisition_frac_autoadjust 50
set_max_bandwidth 40k
# set current range
set_range ba 2100n
set_autoranging ba 2100n 2100n
# set cell on
set_e 0
cell_on
# measurement
store_var j 0i ja
store_var k 0i ja
loop k < 10
  meas_fast_cv e l y 0 -500m 500m 25m 250
  store_var i 0i ja
  loop i < y
    array_get e i w
    array_set m j w
    array_get l i w
    array_set n j w
    add_var i 1i
    add_var j 1i
  endloop
  wait 72m # wait to get the desired rest
  add_var k 1i
endloop
# send the data
store_var i 0i ja
loop i < j
  pck_start
    array_get m i w
    pck_add w
    array_get n i w
    pck_add w
  pck_end
  add_var i 1i
endloop
# set cell off when finished or aborted
on_finished:
  cell_off

'''
method.set_MethodScript(script)
method.Ranging.MaximumCurrentRange =  pspymethods.get_current_range(3)
method.Ranging.MinimumCurrentRange = pspymethods.get_current_range(3)
method.Ranging.StartCurrentRange = pspymethods.get_current_range(3)


if success == 1:
    print('connection established')
    #for ix in range(0,5):
    measurement = manager.measure(method)
    #measurement.measure_async(return_dotnet_object=True)
    if measurement is not None:
        print('measurement finished')
    else:
        print('failed to start measurement')

    success = manager.disconnect()

    if success == 1:
        print('disconnected')
    else:
        print('error while disconnecting')
else:
    print('connection failed')
