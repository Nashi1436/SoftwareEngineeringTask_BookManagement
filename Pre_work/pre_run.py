import os
import django
import sys
from django.conf import settings
from pathlib import Path
import json



#初始化获取信息   
#根据DJANGO_WEB/settings.py 获取信息
#信息存在  根目录/Pre_info/info.txt
#包含 密匙 网站root管理员账户 密码  加密后密码
#     默认root网站管理员为settings 配置数据库配置账户密码

# 获取当前脚本所在的目录的父目录
parent_dir = Path(__file__).resolve().parent.parent

# 设置环境变量，这里'DJANGO_WEB.settings'是您的Django项目设置文件的路径
sys.path.insert(0, str(parent_dir))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DJANGO_WEB.settings')
os.chdir(parent_dir)


# 初始化Django环境
django.setup()

import hashlib
def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    print(settings.SECRET_KEY.encode('utf-8'))
    return obj.hexdigest()


# 获取settings 信息
secret_key = settings.SECRET_KEY
setting_config = settings.DATABASES['default']
root_user = setting_config['USER']
root_password = setting_config['PASSWORD']
root_password_secret=md5(root_password)



# 输出文件路径设置为父目录下的President文件夹
output_file_path = parent_dir / 'Pre_info' / 'info.txt'

dir={
    'secret_key': secret_key,
    'root_user': root_user,
    'root_password': root_password,
    'root_password_secret': root_password_secret,
}

# 将字典转换为JSON格式的字符串
dir_str = json.dumps(dir, indent=4)  # indent参数用于美化输出

# 确保输出目录存在
os.makedirs(parent_dir / 'Pre_info', exist_ok=True)

# 将SECRET_KEY写入到指定文件
with open(output_file_path, 'w') as file:
    file.write(dir_str)

print(f"密匙|root信息 已经写入到 {output_file_path}")







#初始化数据库 

import mysql.connector
# 替换以下变量为您的MySQL连接信息
host = setting_config['HOST']  # MySQL服务器主机名
user = setting_config['USER']  # 您的MySQL用户名
password = setting_config['PASSWORD'] # 您的MySQL密码
database_name = setting_config['NAME']  # 您想要创建的数据库名称

try:
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    cursor = connection.cursor()

    # 创建数据库
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    print(f"Database '{database_name}' created successfully.")

    # 初始化数据库中表 配置在 根目录/app01/models.py
    from django.core.management import call_command
    call_command('makemigrations')
    call_command('migrate')
    print('初始化数据表完成')

    # 插入网站root管理员
    from app01.models import User  # 导入Admin模型
    from django.contrib.auth.hashers import make_password

    # admin_instance, created = User.objects.get_or_create(
    #     username=root_user,
    #     defaults={'password': make_password(root_password_secret)}
    # )
    admin_instance, created = User.objects.get_or_create(
        username=root_user,
        defaults={
            'password': root_password_secret,
            'role': 3,  # 设置角色为ROOT
        }
    )

    if created:
        admin_instance.save()
        print('网站 root 管理添加完成')
    else:
        print('网站 root 管理已存在')

        # 更新密码（假设您要更新密码）
        new_password = root_password_secret  # 新密码
        admin_instance.password = root_password_secret
        admin_instance.save()
        print('网站 root 管理密码已更新')

    print('网站 root管理 账户: '+root_user+"  密码: "+root_password+"  密文: "+root_password_secret)    


except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    # 关闭游标和数据库连接
    if 'cursor' in locals() and cursor is not None:
        cursor.close()
    if 'connection' in locals() and connection is not None:
        connection.close()





