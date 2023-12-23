#!/usr/bin/env python3

import csv
import sys
from datetime import datetime

file_name = sys.argv[1]

with open(file_name, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    
    power_timestamp_old = None
    power_old = None
    counter = 0
    power_summary = 0
    time_summary = 0
    start_time = None
    end_time = None

    speed_timestamp_old = None
    speed_old = None
    distance_total = 0
    speed_sum = 0
    speed_counter = 0

    ambient_temp_sum = 0 
    ambient_temp_counter = 0  

    battery_temp_sum = 0 
    battery_temp_counter = 0

    battery_soh = 0
    battery_soc = 0
    battery_cap = 0
    battery_cap_calculated = 0
    range_calculated = 0

    for row in reader:
        
        counter = counter + 1
        timestring = row['time']
        powerstring = row['HV EV Battery Power (kW)'] 
        speedstring = row['Vehicle speed (km/h)']
        ambient_temp_string = row['Ambient temperature (℃)']
        battery_temp_string = row['DC Battery Temperature (℃)']
        battery_soh_string = row['State of health (%)']
        battery_soc_string = row['State of charge (%)']
        battery_cap_string = row['Battery DC Capacity (kWh)']
        df = datetime.strptime(timestring,'%H:%M:%S.%f')
        seconds = float(df.hour*3600) + float(df.minute*60) + float(df.second) + float(df.microsecond)/1000000
        if not start_time:
           start_time = df 
        end_time = df
        
        if powerstring:
        
            power = float(powerstring)
            
            if power_timestamp_old:
               time_delta = seconds - power_timestamp_old
               power_kwh = power_old * (time_delta/3600) 
               power_summary = power_summary + power_kwh
               time_summary = time_summary + time_delta
               print("calculating power: ", timestring, time_delta, power_old, power_kwh)

            power_timestamp_old = seconds
            power_old = power
        
        if speedstring:
        
           speed = float(speedstring)
           speed_counter = speed_counter + 1
           speed_sum = speed_sum + speed
           
           if speed_timestamp_old:
              time_delta = seconds - speed_timestamp_old
              distance = speed_old * (time_delta/3600)
              distance_total = distance_total + distance
           
           speed_timestamp_old = seconds
           speed_old = speed

        if ambient_temp_string:
           ambient_temp = float(ambient_temp_string)
           ambient_temp_counter = ambient_temp_counter + 1
           ambient_temp_sum = ambient_temp_sum + ambient_temp

        if battery_temp_string:
           battery_temp = float(battery_temp_string)
           battery_temp_counter = battery_temp_counter + 1
           battery_temp_sum = battery_temp_sum + battery_temp

        if battery_soh_string:
           battery_soh = float(battery_soh_string)

        if battery_soc_string:
           battery_soc = float(battery_soc_string)

        if battery_cap_string:
           battery_cap = float(battery_cap_string)

        if battery_soc > 0 and battery_cap > 0 :
           battery_cap_calculated_new = ( battery_cap / battery_soc ) * 100   
           if battery_cap_calculated_new > battery_cap_calculated:
              battery_cap_calculated = battery_cap_calculated_new


time_interval = end_time - start_time
average_speed = speed_sum / speed_counter
average_consumption = power_summary / (distance_total/100)
avg_amb_temperature = ambient_temp_sum / ambient_temp_counter 
ave_bat_temperature = battery_temp_sum / battery_temp_counter 
max_range_estimated = ( battery_cap_calculated / average_consumption ) * 100

print("")
print("### Trip:", file_name)
print("| Variable        | Value                                      |")
print("|-----------------|--------------------------------------------|")
print("| trip time       | ", time_interval, "|")
print("| power consumed  | ", round(power_summary, 2), "kWh", "  |")
print("| distance        | ", round(distance_total, 2), "km", "  |")
print("| avg. speed      | ", round(average_speed, 2), "km/h", "  |")
print("| avg. consumtion | ", round(average_consumption, 2), "kWh/100km", "  |")
print("| avg. amb. temp. | ", round(avg_amb_temperature, 2), "℃", "  |")
print("| avg. bat. temp. | ", round(ave_bat_temperature, 2), "℃", "  |")
print("| battery SoH     | ", round(battery_soh, 2), "%", "  |")
print("| max battery cap.| ", round(battery_cap_calculated, 2), "kWh", "  |")
print("| max range estim.| ", round(max_range_estimated, 2), "km", "  |")
print("| car setup       | NA  |")
print("| weather         | NA  |")
print("| road condition  | NA  |")
print("")



