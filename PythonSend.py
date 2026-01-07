#CODE: need to test getLatestTemp() on actual DR

from so3g.hk import load_range
#import datetime
import datetime as dt
import serial
import time

#stop = dt.datetime(2025, 7, 8, 23, 35, tzinfo=dt.timezone.utc)
#start = dt.datetime(2025, 7, 8, 19, 34, tzinfo=dt.timezone.utc)

#loading fields for channels 2,6
#field2 = ["observatory.LSA2S5J.feeds.temperatures.Channel_02_T"]
#field6 = ["observatory.LSA2S5J.feeds.temperatures.Channel_06_T"]

#loading data for channels 2,6
#data2 = load_range(start, stop, field2, data_dir="/Users/debbiewang/Documents/Research")
#data6 = load_range(start, stop, field6, data_dir="/Users/debbiewang/Documents/Research")

#TESTING: printing everything out
#print("CHANNEL 2 \n", data2)
#print("CHANNEL 6 \n", data6)

#double arrays of time and temperature
#timestamps2, values2 = data2["observatory.LSA2S5J.feeds.temperatures.Channel_02_T"]
#timestamps6, values6 = data6["observatory.LSA2S5J.feeds.temperatures.Channel_06_T"]

#figuring out which channel to poll
data = {}

#if 0 < values6[-1] < 4:                    
#    data = (timestamps6, values6)
#elif values2[-1] < 300:  
#    data = (timestamps2, values2)
#else:
#    data = ([],[])

#finding temperature
timestamps, values = data
#print("TEMP:", values[-1])

def get_latest_temp():
    stop = dt.datetime.now(dt.timezone.utc)
    start = stop - dt.timedelta(minutes=4)

    field2 = ["observatory.LSA2S5J.feeds.temperatures.Channel_02_T"]
    field6 = ["observatory.LSA2S5J.feeds.temperatures.Channel_06_T"]

    data2 = load_range(start, stop, field2, data_dir="/Users/debbiewang/Documents/Research")
    data6 = load_range(start, stop, field6, data_dir="/Users/debbiewang/Documents/Research")

    timestamps2, values2 = data2["observatory.LSA2S5J.feeds.temperatures.Channel_02_T"]
    timestamps6, values6 = data6["observatory.LSA2S5J.feeds.temperatures.Channel_06_T"]

    if 0 < values6[-1] < 4:
        return values6[-1]
    elif values2[-1] < 300:
        return values2[-1]
    else:
        return None

arduino = serial.Serial(port='/dev/cu.usbmodem1101', baudrate=9600, timeout=10)
time.sleep(5)

#decoding arduino's response
def write_read(x): 
    #arduino.write(bytes(x,'utf-8')) #sending to arduino
    #time.sleep(0.05)
    return arduino.readline().decode('utf-8').strip() #reading arduino

while True:
    temp_value = get_latest_temp()
    if temp_value is not None:
        temp_str = f"{temp_value:.3f}\n"
        arduino.write(bytes(temp_str.encode('utf-8')))
        time.sleep(0.05)
        response = arduino.readline().decode("utf-8",errors="ignore").strip()
        #response = write_read(temp_str) #reading arduino's response
        print("Arduino replied:", response)
    else:
        print("No valid temperature found.")
    
    time.sleep(120)  # Wait 2 minutes
