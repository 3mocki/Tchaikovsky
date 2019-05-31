import time, csv, board, busio
import RPi.GPIO as GPIO
import adafruit_ads1x15.ads1115 as ADS
from Average1 import *
from Average2 import *
from Average3 import *
from Sender import *
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)

# air list; ppm is O3 and CO // ppb is NO2, SO2
air_list = ['no2', 'o3', 'co', 'so2', 'pm25', 'pm10']

# timestamp, temp, no2, o3, co, so2, pm25, pm10, i, m
data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# WE_e // calibration data of 25-000160 Indoor Sensor, Unit is mV
we_zero = [295, 391, 247, 387]
ae_zero = [283, 389, 269, 275]
sens = [0.228, 0.399, 0.267, 0.318]

# Follow the 803-05
temp_n = [[0.8, 0.8, 1, 1.2, 1.6, 1.8, 1.9, 2.5, 3.6],
          [0.1, 0.1, 0.2, 0.3, 0.7, 1, 1.7, 3, 4],
          [1, 1, 1, 1, -0.2, -0.9, -1.5, -1.5, -1.5],
          [0, 0, 0, 0, 0, 0, 5, 25, 45]]


# pin number initialization
path_val= [17, 27, 22, 5]

numberOfData = 0
csvRowCount = 0

# set the gpio pins to OUTPUT mode
def init_gpio():
    for pin in path_val:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

# mux controlling function
def mux_control(num):
    init_gpio()
    if num % 2 == 1:
        GPIO.output(path_val[0], 1)
    if num % 4 > 1:
        GPIO.output(path_val[1], 1)
    if num % 8 > 3:
        GPIO.output(path_val[2], 1)
    if num % 16 > 7:
        GPIO.output(path_val[3], 1)


def temp_choice(tmp, x):
    if -30 > tmp:
        return temp_n[x - 1][0]
    elif -30 <= tmp < -20:
        return temp_n[x - 1][1]
    elif -20 <= tmp < -10:
        return temp_n[x - 1][2]
    elif -10 <= tmp < 0:
        return temp_n[x - 1][3]
    elif 0 <= tmp < 10:
        return temp_n[x - 1][4]
    elif 10 <= tmp < 20:
        return temp_n[x - 1][5]
    elif 20 <= tmp < 30:
        return temp_n[x - 1][6]
    elif 30 <= tmp < 40:
        return temp_n[x - 1][7]
    elif 40 <= tmp <= 50:
        return temp_n[x - 1][8]

def write_rad(numberOfData, csvRowCount):
    if csvRowCount + 1 == 10:
        f = open('temp_RAD.csv', 'w', newline='')
        f.truncate()
        wr = csv.writer(f)

        for i in air_sender:
            wr.writerow(i)
        f.close()
        numberOfData += 1
        csvRowCount = 0

    else:
        numberOfData += 1
        csvRowCount += 1
    return numberOfData, csvRowCount

def collect_Data():
    # collecting air data
    for x in range(0, 6):
        init_gpio()
        print('*******************************')
        if x == 0:
            # measuring temperature
            mux_control(x)
            ads = ADS.ADS1115(i2c)
            chan = AnalogIn(ads, ADS.P0)
            temp_value = chan.voltage * 1000
            temp_result = (float(temp_value) - 500) * 0.1 # 500 is offset & 0.1 is Output Voltage Scaling
            if temp_result <= -30:
                temp_result = -30
            elif temp_result > 50:
                temp_result = 50
            print('Temperature : ' + str(round(temp_result, 2)) + 'degree celcius')
            # choice temperature each sensor
            data[1] = round(temp_result, 2)

        elif 1 <= x <= 4:
            # Measuring Working Electrode
            mux_control(x * 2 - 1)
            ads = ADS.ADS1115(i2c)
            chan = AnalogIn(ads, ADS.P0)
            we_value = chan.voltage * 1000
            print(air_list[x - 1] + ' WE : ' + str(round(we_value, 2)) + 'mV')

            # Measuring Auxiliary Electrode
            mux_control(x * 2)
            ads = ADS.ADS1115(i2c)
            chan = AnalogIn(ads, ADS.P0)
            ae_value = chan.voltage * 1000
            print(air_list[x - 1] + ' AE : ' + str(round(ae_value, 2)) + 'mV')

            if x == 1:
                temp = temp_choice(temp_result, x)
                # calculating ppb & ppm
                ppb_value = ((we_value - we_zero[x - 1]) - temp * (ae_value - ae_zero[x - 1])) / \
                            sens[x - 1]
                no2 = round(ppb_value, 3)
                data[2] = no2
                print(air_list[x - 1] + ' : ' + str(no2) + 'ppb')

            elif x == 2:
                temp = temp_choice(temp_result, x)
                # calculating ppb & ppm
                ppb_value = ((we_value - we_zero[x - 1]) - (0 - (-1))) - temp * (ae_value - ae_zero[x - 1]) / \
                            sens[x - 1]
                o3 = round(ppb_value / 1000, 3)
                data[3] = o3
                print(air_list[x - 1] + ' : ' + str(o3) + 'ppm')

            elif x == 3:
                temp = temp_choice(temp_result, x)
                # calculating ppb & ppm
                ppb_value = ((we_value - we_zero[x - 1]) - temp * (ae_value - ae_zero[x - 1])) / \
                            sens[x - 1]
                co = round(ppb_value / 1000, 3)
                data[4] = co
                print(air_list[x - 1] + ' : ' + str(co) + 'ppm')

            elif x == 4:
                temp = temp_choice(temp_result, x)
                # calculating ppb & ppm
                ppb_value = ((we_value - we_zero[x - 1])) - temp / \
                            sens[x - 1]
                so2 = round(ppb_value, 3)
                data[5] = so2
                print(air_list[x - 1] + ' : ' + str(so2) + 'ppb')

            print('n Table = > ' + str(temp))

        elif x == 5:
            mux_control(x * 2 - 1)
            ads = ADS.ADS1115(i2c)
            chan = AnalogIn(ads, ADS.P0)
            pm25_value = chan.voltage
            v = pm25_value
            hppcf = 240 * (v ** 6) - 2491.3 * (v ** 5) + 9448.7 * (v ** 4) - 14840 * (v ** 3) + 10684 * (
                    v ** 2) + 2211.8 * v + 7.9623
            ugm3 = .518 + .00274 * hppcf
            pm25 = round(ugm3, 3)
            data[6] = pm25
            pm10 = round(ugm3, 3)
            data[7] = pm10
            print(air_list[x - 1] + ' : ' + str(pm25) + 'ug/m^3')
            print(air_list[x] + ' : ' + str(pm10) + 'ug/m^3')
            print('*******************************')

def save_to_DS(r, z):
    if r % 10 == z:
        air_sender[z][0] = data[0]  # timestamp
        air_sender[z][5] = data[1]  # temp
        air_sender[z][8] = data[2]  # no2
        air_sender[z][7] = data[3]  # o3
        air_sender[z][6] = data[4]  # co
        air_sender[z][9] = data[5]  # so2
        air_sender[z][10] = data[6]  # pm10
        air_sender[z][11] = data[7]  # pm25

if __name__ == '__main__':
    print("=========Operating Sensor=========")

    av1 = Average_1
    av2 = Average_8
    av3 = Average_24

    init_time = int(time.time())
    try:
        while True:
            init_time += 1
            data[0] = init_time
            start = time.time()
            data[8] = numberOfData
            data[9] = csvRowCount

            print('Data Number:' + str(data[8]))
            print('CSVR Number:' + str(data[9]))

            collect_Data()

            av1.insertData(1, 2, 3, 4, 5)  # no2, o3, so2
            #av1.insertData(data[2], data[3], data[5], data[8], data[9])  # no2, o3, so2
            av2.insertData(data[3], data[4], data[8], data[9])  # o3, co
            av3.insertData(data[6], data[7], data[8], data[9])  # pm10, pm25

            save_to_DS(numberOfData, csvRowCount)
            # write_raw()
            numberOfData, csvRowCount = write_rad(numberOfData, csvRowCount)

            end = time.time()
            sensing = end - start
            print("delayed : " + str(end - start) + " sec")
            timegap = 1 - sensing
            print("timegap : " + str(timegap) + " sec")
            time.sleep(timegap)

    except KeyboardInterrupt:
        print("Stop Operating")
        print("Exit")