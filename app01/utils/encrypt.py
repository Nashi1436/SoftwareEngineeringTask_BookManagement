from django.conf import settings
import hashlib


def md5(data_string):
    print(settings.SECRET_KEY.encode('utf-8'))
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    
    return obj.hexdigest()
