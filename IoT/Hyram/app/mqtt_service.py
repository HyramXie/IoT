from .services import get_mqtt


def start_mqtt_listener():
    client = get_mqtt()
    client.connect()
    client.subscribe('raspberry')
    client.start_loop()
    # # 启动 MQTT 客户端的循环处理线程
    # mqtt_thread = threading.Thread(target=client.loop_forever)
    # mqtt_thread.daemon = True  # 设置为守护线程
    # mqtt_thread.start()
    # print("MQTT listener started.")
