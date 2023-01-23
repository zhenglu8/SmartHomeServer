import re #import re library for regular expression
import subprocess #import subprocess library for another python library
from influxdb import InfluxDBClient #import influxDBClient to interact with influxDB server

#use subprocess to call Speedtest CLI and then we store and decode the response variable
response = subprocess.Popen('/usr/bin/speedtest', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

#use re library to do regular expression
ping = re.search('Latency:\s+(.*?)\s', response, re.MULTILINE)
download = re.search('Download:\s+(.*?)\s', response, re.MULTILINE)
upload =  re.search('Upload:\s+(.*?)\s', response, re.MULTILINE)

#use group function to extract correct numbers from regular expression
ping = ping.group(1)
download = download.group(1)
upload = upload.group(1)

#test ping, download speed, upload data and save as csv file
"""
try:
    f = open('/home/pi/speedtest/speedtest.csv', 'a+')
    if os.stat('/home/pi/speedtest/speedtest.csv').st_size == 0:
            f.write('Date,Time,Ping (ms),Download (Mbps),Upload (Mbps)\r\n')
except:
    pass
"""

#format the data to be JSON like format using Python dictionary
#the measurement of database is internet_speed
#the three fields of database are: download, uoload, and ping
speed_data = [
    {
        "measurement" : "internet_speed",
        "tags" : {
            "host": "RaspberryPiMyLifeUp"
        },
        "fields" : {
            "download": float(download),
            "upload": float(upload),
            "ping": float(ping)
        }
    }
]
#pass five parameters to influxDB server: host, port, username, password, database name
client = InfluxDBClient('localhost', 8086, 'speedmonitor', 'pimylifeup', 'internetspeed')
#write data pointing to the influxDB server
client.write_points(speed_data)