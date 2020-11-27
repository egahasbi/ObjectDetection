import time, datetime
import telepot
from telepot.loop import MessageLoop
import threading
import serial              
from time import sleep
import sys

        
def task2():
    global map_link
    ser = serial.Serial ("COM7")
    gpgga_info = "$GPGGA,"
    GPGGA_buffer = 0
    NMEA_buff = 0

    def convert_to_degrees(raw_value):
        decimal_value = raw_value/100.00
        degrees = int(decimal_value)
        mm_mmmm = (decimal_value - int(decimal_value))/0.6
        position = degrees + mm_mmmm
        position = "%.4f" %(position)
        return position

    try:
        while True:
            received_data = (str)(ser.readline()) #read NMEA string received
            GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                
            if (GPGGA_data_available>0):
                GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after “$GPGGA,” string
                NMEA_buff = (GPGGA_buffer.split(','))
                nmea_time = []
                nmea_latitude = []
                nmea_longitude = []
                nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
                nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
                nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
                print("NMEA Time: ", nmea_time,'\n')
                lat = nmea_latitude
                lat = convert_to_degrees(float(lat))
                longi = nmea_longitude
                longi = convert_to_degrees(float(longi))
                print ("NMEA Latitude:", lat,"NMEA Longitude:", longi,'\n')           
                map_link = 'http://maps.google.com/?q=-' + lat + ',' + longi
                print(map_link)
    except KeyboardInterrupt:
        sys.exit(0)

def task1():
    global map_link
    now = datetime.datetime.now()
    def action(msg):
        chat_id = msg['chat']['id']
        command = msg['text']
        print ("Received: %s", command)
        if command == '/wiwik':
            telegram_bot.sendMessage (chat_id, str("I Love You"))
        if command == '/lokasi':
            telegram_bot.sendMessage (chat_id, map_link)    
    telegram_bot = telepot.Bot('1314577893:AAFBD0LOisPKaUSinfYMVm4sVERKNT-J4iA')
    print (telegram_bot.getMe())
    MessageLoop(telegram_bot, action).run_as_thread()
    print ('Up and Running....')
    # while 1:
    #     time.sleep(10)        


if __name__ == "__main__":
         t1 = threading.Thread(target=task1)
         t2 = threading.Thread(target=task2)
         t1.start()
         t1.join()
         t2.start()
         t2.join()
    