import traceback
import pspython.pspydata as pspydata

# Import the static LoadSaveHelperFunctions
from PalmSens.Windows import LoadSaveHelperFunctions
from PalmSens.Data import SessionManager


def load_session_file(path, **kwargs):
    load_peak_data = kwargs.get('load_peak_data', False)
    load_eis_fits = kwargs.get('load_eis_fits', False)
    return_dotnet_object = kwargs.get('return_dotnet_object', False)

    try:
        session = LoadSaveHelperFunctions.LoadSessionFile(path)
        measurements_with_curves = {}

        for m in session:
            measurements_with_curves[pspydata.convert_to_measurement(m, load_peak_data=load_peak_data, load_eis_fits=load_eis_fits, return_dotnet_object=return_dotnet_object)] = pspydata.convert_to_curves(m)

        return measurements_with_curves
    except:
        traceback.print_exc()
        print(error)
        return 0


def save_session_file(path, measurement):
    if measurement.dotnet_measurement is None:
        raise Exception('cannot save measurements that do not have a reference to the dotnet measurement object')
    
    try:
        session = SessionManager()
        session.MethodForEditor = measurement.dotnet_measurement.Method
        session.AddMeasurement(measurement.dotnet_measurement)

        LoadSaveHelperFunctions.SaveSessionFile(path, session)
        return
    except:
        traceback.print_exc()
        print(error)
        return 0


def save_session_file(path, measurements):
    for measurement in measurements:
        if measurement.dotnet_measurement is None:
            raise Exception('cannot save measurements that do not have a reference to the dotnet measurement object')
    
    try:
        session = SessionManager()
        session.MethodForEditor = measurements[0].dotnet_measurement.Method

        for measurement in measurements:
            session.AddMeasurement(measurement.dotnet_measurement)

        LoadSaveHelperFunctions.SaveSessionFile(path, session)
        return
    except:
        traceback.print_exc()
        print(error)
        return 0        


def read_notes(path, n_chars=3000):
    with open(path, 'r', encoding="utf16") as myfile:
        contents = myfile.read()
    raw_txt = contents[1:n_chars].split('\\r\\n')
    notes_txt = [x for x in raw_txt if 'NOTES=' in x]
    notes_txt = notes_txt[0].replace('%20', ' ').replace('NOTES=', '').replace('%crlf', os.linesep)
    return notes_txt


def load_method_file(path):
    try:
        method = LoadSaveHelperFunctions.LoadMethod(path)
        return method
    except:
        return 0


def get_method_estimated_duration(path):
    method = load_method_file(path)
    if method == 0:
        return 0
    else:
        return method.MinimumEstimatedMeasurementDuration

