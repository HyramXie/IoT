import time

from django.http import JsonResponse, HttpResponse, HttpRequest
from .services import get_mqtt
from .models import Information
from .mqtt_service import start_mqtt_listener
import json


# Create your views here.

def get_now_info(request):
    mqtt = get_mqtt()
    mqtt.connect()
    # 立刻获取，并且读取数据库最新信息
    mqtt.publish_message("nowInfo", "1")
    time.sleep(5)
    information = Information.objects.last()
    data = {
        'temperatures': information.temperature,
        'humidity': information.humidity,
        'moisture': information.moisture,
        'time': information.created_at,
    }
    return JsonResponse(data)


def get_chart_info(request):
    informations = Information.objects.all().order_by('created_at')[:20]

    humidity = [float(information.humidity) for information in informations]
    temperature = [float(information.temperature) for information in informations]
    moisture = [float(information.moisture) for information in informations]
    time = [information.created_at.strftime('%Y-%m-%d %H:%M:%S') for information in informations]

    data = {
        'temperatures': temperature,
        'humidity': humidity,
        'moisture': moisture,
        'time': time,
    }

    return JsonResponse(data)


def set_info(request):
    print("request Get:", request.GET)
    threshold = float(request.GET['threshold'])
    print(threshold)
    mqtt = get_mqtt()
    mqtt.connect()
    data = json.dumps({
        "threshold": threshold,
    })
    mqtt.publish_message('windows', data)
    return HttpResponse(status=200)


start_mqtt_listener()
