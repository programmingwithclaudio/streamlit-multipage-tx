import streamlit as st
import requests
import urllib
import os
from dotenv import load_dotenv
import toml


st.title('EcoMove')

vehicle_type = st.radio("Select vehicle type:", ('fuel', 'electric'))

if vehicle_type == 'fuel':
    origin = st.text_input("Enter origin:")
    destination = st.text_input("Enter destination:")
    consumption = st.number_input("Enter fuel consumption (in km/l): ")
    if st.button('Calculate'):
        url = api_url + urllib.parse.urlencode({"key":key, "from":origin, "to":destination, "routeType": "fastest", "unit": "k"})
        json_data = requests.get(url).json()
        status_code = json_data['info']['statuscode']
        if status_code == 0:
            trip_duration_seconds = json_data['route']['time']
            trip_duration_hours = trip_duration_seconds / 3600
            distance = json_data['route']['distance']
            st.write('==========================================')
            st.write(f'Trip information {origin} to {destination}')
            st.write(f'The duration of the trip is {trip_duration_hours:.2f} hours')
            st.write(f'The distance to the destinations is {distance} KM')

            total_fuel_consumption = distance / consumption
            st.write(f'Total fuel consumption for the trip: {total_fuel_consumption:.2f} liters')

            factor_emision_co2_kg = 8.89  # en kg/galón
            total_co2_emissions_kg = total_fuel_consumption * factor_emision_co2_kg
            st.write(f'Average CO2 emissions for the trip: {total_co2_emissions_kg:.2f} kilograms')

            traffic_data = requests.get(traffic_url + urllib.parse.urlencode({"key": key, "boundingBox": f"{json_data['route']['boundingBox']['ul']['lat']},{json_data['route']['boundingBox']['ul']['lng']},{json_data['route']['boundingBox']['lr']['lat']},{json_data['route']['boundingBox']['lr']['lng']}"})).json()
            if 'incidents' in traffic_data and traffic_data['incidents']:
                st.write("There are incidents on the route that could delay the trip.")
            else:
                st.write("No incidents on the route.")

            average_speed = distance / trip_duration_hours
            st.write(f"Average speed: {average_speed:.2f} km/h")

elif vehicle_type == 'electric':
    origin = st.text_input("Enter origin:")
    destination = st.text_input("Enter destination:")
    if st.button('Calculate'):
        result = funcs.find_charging_stations(origin, destination)
        for line in result:
            st.write(line)
        
        url = api_url + urllib.parse.urlencode({"key":key, "from":origin, "to":destination, "routeType": "fastest", "unit": "k"})
        json_data = requests.get(url).json()
        status_code = json_data['info']['statuscode']
        if status_code == 0:
            trip_duration_seconds = json_data['route']['time']
            trip_duration_hours = trip_duration_seconds / 3600
            distance = json_data['route']['distance']
            
            st.write('==========================================')
            st.write(f'Trip information {origin} to {destination}')
            st.write(f'The duration of the trip is {trip_duration_hours:.2f} hours')
            st.write(f'The distance to the destinations is {distance} KM')

            traffic_data = requests.get(traffic_url + urllib.parse.urlencode({"key": key, "boundingBox": f"{json_data['route']['boundingBox']['ul']['lat']},{json_data['route']['boundingBox']['ul']['lng']},{json_data['route']['boundingBox']['lr']['lat']},{json_data['route']['boundingBox']['lr']['lng']}"})).json()
            if 'incidents' in traffic_data and traffic_data['incidents']:
                st.write("There are incidents on the route that could delay the trip.")
            else:
                st.write("No incidents on the route.")

            average_speed = distance / trip_duration_hours
            st.write(f"Average speed: {average_speed:.2f} km/h")
