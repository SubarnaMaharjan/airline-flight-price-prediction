import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

def date_conv():
    data = pd.read_excel(r'/home/vylericd3vil/Minor-project/Dataset/Data_Train.xlsx')

    data["Journey_day"] = pd.to_datetime(data.Date_of_Journey, format="%d/%m/%Y").dt.day

    data["Journey_month"] = pd.to_datetime(data["Date_of_Journey"], format = "%d/%m/%Y").dt.month


    data.drop(["Date_of_Journey"], axis = 1, inplace = True)


    
def time_conv(data,Time,hour,min):  #Arrival_Time,Departure_Time
    data[hour] = pd.to_datetime(data[Time]).dt.hour


    data[min] = pd.to_datetime(data[Time]).dt.minute


    data.drop(["Time"], axis = 1, inplace = True)

      

def duration_conv(data):
    duration = list(data["Duration"])

    for i in range(len(duration)):
        if len(duration[i].split()) != 2:   
            if "h" in duration[i]:
                duration[i] = duration[i].strip() + " 0m"  
            else:
                duration[i] = "0h " + duration[i]  
    duration_hours = []
    duration_mins = []
    for i in range(len(duration)):
        duration_hours.append(int(duration[i].split(sep = "h")[0]))  
        duration_mins.append(int(duration[i].split(sep = "m")[0].split()[-1]))

    data["Duration_hours"] = duration_hours
    data["Duration_mins"] = duration_mins

    data.drop(["Duration"], axis = 1, inplace = True)

