from so3g.hk import load_range
import datetime as dt
import serial
import time

data = {}

#finding temperature
timestamps, values = data

def get_latest_temp():
    #polling the most recent temperature
    stop = dt.datetime.now(dt.timezone.utc)
    start = stop - dt.timedelta(minutes=4)

    field2 = ["observatory.LSA2S5J.feeds.temperatures.Channel_02_T"]
    field6 = ["observatory.LSA2S5J.feeds.temperatures.Channel_06_T"]

    #loading data for channels 2,6
    data2 = load_range(start, stop, field2, data_dir="/Users/debbiewang/Documents/Research")
    data6 = load_range(start, stop, field6, data_dir="/Users/debbiewang/Documents/Research")

    #double arrays of time and temperature
    timestamps2, values2 = data2["observatory.LSA2S5J.feeds.temperatures.Channel_02_T"]
    timestamps6, values6 = data6["observatory.LSA2S5J.feeds.temperatures.Channel_06_T"]

    #determining which thermometer to poll
    if 0 < values6[-1] < 4: #cold stage
        return values6[-1]
    elif values2[-1] < 300: #initial cooling
        return values2[-1]
    else: #DR is room temperature
        return None

#communicating with arduino
arduino = serial.Serial(port='/dev/cu.usbmodem1101', baudrate=9600, timeout=10)
time.sleep(5)

#decoding arduino's response
def write_read(x): 
    #arduino.write(bytes(x,'utf-8')) #sending to arduino
    #time.sleep(0.05)
    return arduino.readline().decode('utf-8').strip() #reading arduino

#receiving arduino's response
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
