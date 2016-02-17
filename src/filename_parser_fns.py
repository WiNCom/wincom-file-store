import re
from datetime import datetime

LOCATION_MAP = {
    'iitso': 'IIT Spectrum Observatory',
    'tower': 'IIT Spectrum Observatory',
    'chicago': 'Mobile - Chicago',
    'harbor': 'Harbor Point',
    'hp': 'Harbor Point',
}

SENSOR_MAP = {
    'rfeye': 'RFeye',
    'iitso': 'Rohde Schwarz Spectrum Analyzer',
    'xg': 'RC Sensor',
}


def site_from_name(filename):
    split_file = filename.split('_')

    for token in split_file:
        if token.lower() in LOCATION_MAP:
            return LOCATION_MAP[token.lower()]

    return 'Unknown'


def sensor_from_name(filename):
    split_file = filename.split('_')
    for token in split_file:
        if token.lower() in SENSOR_MAP:
            return SENSOR_MAP[token.lower()]

    return 'Unknown'


def measurement_type_from_name(filename):
    return 'power_spectrum'


def date_from_name(filename):
    if filename.split('.')[-1] == 'bin':
        file_date = _file_date_from_rfeye_name(filename)
    else:
        file_date = _file_date_from_hdf_name(filename)

    if file_date != 'Unknown':
        return file_date.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return file_date


def _file_date_from_rfeye_name(filename):
    numbers = re.findall(r"\d+", filename)
    if len(numbers) == 0:
        return 'Unknown'
    else:
        file_date = '20{0}'.format(numbers[0][:6])
        file_time = '{0}'.format(numbers[1])
        file_datetime = '{0}{1}'.format(file_date, file_time)
        return datetime.strptime(file_datetime, "%Y%m%d%H%M%S")


def _file_date_from_hdf_name(filename):
    numbers = re.findall(r"\d+", filename)
    if len(numbers) == 0:
        return 'Unknown'
    else:
        file_date = numbers[0][:8]
        return datetime.strptime(file_date, "%Y%m%d")


def format_from_name(file_to_store):
    extension = file_to_store.split('.')[-1]
    if extension == 'bin':
        return 'RFEye'
    else:
        return 'HDF5'
