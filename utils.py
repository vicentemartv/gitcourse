import requests
import json
import pandas as pd

# accesos
API_KEY = '--------------------------------------------'  # <- Your API key goes here
URL = 'https://api.machinemetrics.com/reports/production'
headers = {'Authorization': f'Bearer {API_KEY}',
           'Content-type': 'application/json'}


def fetch_data(payload):
    response = requests.post(URL, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        json_response = response.json()
        data = json_response['items']
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None


def procesar_reporte(id_reporte, data):
    # Lógica para procesar los datos del reporte según el ID del reporte
    dataframe = pd.DataFrame(data)

    if id_reporte == "ID_reporte_1":
        dataframe = dataframe.rename(columns={'day': 'date'})
        dataframe['date'] = pd.to_datetime(dataframe['date'])
        dataframe['day'] = dataframe['date'].dt.day_name()
        dataframe['date'] = dataframe['date'].dt.date
        dataframe['timeInCycle'] = dataframe['timeInCycle'].apply(convert_time)
        dataframe['allTime'] = dataframe['allTime'].apply(convert_time)
        dataframe = dataframe[dataframe['shift'] != 'No Shift']
        column_order = ['date', 'day', 'shift', 'shiftId',
                        'machine', 'machineGroup', 'timeInCycle', 'allTime']
        dataframe = dataframe[column_order]

    elif id_reporte == "ID_reporte_2":
        print('Aqui va algo XD')

    return dataframe


def convert_time(miliseconds):
    """Convert time from miliseconds to hours."""
    hours = miliseconds / (100*60*60)
    return round(hours, 2)


def convert_percentage(percentage):
    """Convert Utilization Rate to correct percentage"""
    percentage = round(percentage * 100, 1)
    return percentage
