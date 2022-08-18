from os import path
import datetime as dt


# list name aria where weather station are
location_list = ['WFR', 'WWA', 'Depot', 'Dixie']

# it is meaning aliases from raw data which come from weather station
terms_dict = {
    '@I': 'IMEI', '@0': 'Type Message version', 'N': 'Message number', 'T': 'Time', 'B': 'Battery', 'LA': 'Latitude',
    'LO': 'Longitude', 'EL': 'Elevation', 'OR': 'Orientation', 'TA': 'Temperature', 'BA': 'Barometric pressure',
    'RH': 'Relative humidity', 'WI': 'Wind speed & direction', 'GU': 'Peak wind & direction',
    'LD': 'Lightning distance', 'CL': 'Cloud height', 'PW': 'Present weather', 'VI': 'Visibility',
    'XA': 'Raw sensor data', 'XD': 'System diagnostics',
}
# list aliases which have a more than one meaning
terms_for_upg = [
    'N', 'B', 'EL', 'OR', 'BA', 'WI',
    'GU', 'LD', 'CL', 'PW', 'XA', 'XD'
]


# transform raw data into a dictionary, creating a dictionary for the required values,
# adding keys to the dictionary.
def data_handler(location):
    data = {}
    parent_dir = path.dirname(path.abspath(__file__))

    with open(path.join(parent_dir, 'location', location), "r") as data_file:
        raw_data = data_file.readlines()
    try:
        for line in raw_data:
            a = line.replace(':', ' ', 1).replace('\n', '').split(' ')
            for i in terms_dict.keys():
                if i == a[0]:
                   data[i] = a[1]

        for i in terms_for_upg:
            tmp_dict = {}
            tmp_list = data[i].replace(':', ' ').split(' ')

            for j in range(len(tmp_list)):
                tmp_dict[j+1] = tmp_list[j]

            data[i] = tmp_dict

        return data
    except Exception as ex:
        print(ex)
        return None


# Check the 'T'- last connection time if time more than 3 hours connection is lost !Alarm!
def time_control(data):
    d_data = dt.datetime.strptime(data, "%y/%m/%d,%H:%M:%S")
    if (d_data + dt.timedelta(hours=3)) > dt.datetime.now():
        return True
    return False
#


# returns the direction of the wind in the value of the wind rose
def wind_direction(degree):
    cardinal_direct = [' N', 'NI', ' I', 'SI', ' S', 'SW', ' W', 'NW']
    for i in range(0, 8):
        step = 45.
        min_deg = i*step - 45/2.
        max_deg = i*step + 45/2.
        if i == 0 and degree > 360-45/2.:
            degree = degree - 360
        if degree >= min_deg and degree <= max_deg:
            result = cardinal_direct[i]
            break
    return(result)


def main():
    print(location_list)


if __name__ == '__main__':
    main()
