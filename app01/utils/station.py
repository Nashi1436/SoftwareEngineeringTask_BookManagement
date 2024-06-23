import random
from django.utils import timezone

def get_station(name):
    # 生成监测站站数据
    data = {
        'name': name,
        'wendu': random.uniform(-30, 50),  # 假设温度范围是 -30 到 50
        'fengsu': random.uniform(0, 100),  # 假设风速范围是 0 到 100
        'shidu': random.uniform(0, 100),   # 假设湿度范围是 0 到 100
        'pm25': random.uniform(0, 500),    # 假设 PM2.5 范围是 0 到 500
        'create_time': timezone.now()      # 使用当前时间
    }

    return data