# Importing modules
import spidev  # To communicate with SPI devices
from numpy import interp  # To scale values
import time  # To add delay
import RPi.GPIO as GPIO
from sensor import MCP3004
import paho.mqtt.client as mqtt
import Adafruit_DHT
import time
import json
import threading


# 当服务器响应的时候，会回调这个函数
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # 订阅 raspberry/topic 主题
    client.subscribe("windows")
    client.subscribe("nowInfo")

# 回调函数，当收到消息时，触发该函数
def on_message(client, userdata, msg):
    global threshold, interval_time
    print(f"{msg.topic} {msg.payload}")
    if msg.topic == 'windows':
        threshold = json.loads(msg.payload.decode())['threshold']
        #interval_time = json.loads(msg.payload.decode())['time']
    elif msg.topic == 'nowInfo':
        get_info()

def get_info():
    moisture = mcp.read(0)  # Reading from CH0
    moisture = interp(moisture, [0, 1023], [100, 0])
    moisture = int(moisture)
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
    if humidity is not None and temperature is not None:
        telemetry = json.dumps({
            'humidity': humidity,
            'temperature': temperature,
            'moisture': moisture
            })
        print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature,humidity))
        print(f"send Moisture:{moisture} to raspberry/")
        client.publish('raspberry', payload=telemetry, qos=0, retain=False)
    else:
        print('Failed to get reading. Try again!')
    return humidity, temperature, moisture

def loop_detect():
    humidity, temperature, moisture = get_info()  # Reading from CH0
    #print(moisture)
    # 数值越大越干燥 对于植物来说，一般大于400则可以进行浇水。
    if moisture > threshold:
        # 进行控制开关水，每次浇水10秒钟
        GPIO.setup(watering_channel, GPIO.OUT)
        GPIO.output(watering_channel,GPIO.LOW)
        time.sleep(10)
        GPIO.setup(watering_channel, GPIO.OUT)
        GPIO.output(watering_channel, GPIO.HIGH)
    

def set_interval(fn):
    timer = {"leap":True}
    def action():
        fn()
        temp()
    def temp():
        if timer['leap']:
            threading.Timer(interval_time,action).start()
    temp()
    return timer

#device init
watering_channel = 17
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
mcp = MCP3004(bus=0, addr=0, vref=3.3)
mcp._spi.max_speed_hz = 2106000

#sensor init
sensor = Adafruit_DHT.DHT11
gpio = 23

#variable
threshold = 400
interval_time = 60

#mqtt init
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.emqx.io", 1883, 60)
# 设置遗嘱消息（立遗嘱），当树莓派断电，或者网络出现异常中断时，发送遗嘱消息往这个 topic
client.will_set('watering/testament', b'{"status": "Off"}')

#run
set_interval(loop_detect)

# 设置网络循环堵塞，在调用 disconnect() 或程序崩溃前，不会主动结束程序
client.loop_forever()



