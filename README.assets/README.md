# PythonDjango课程项目

[项目地址](https://github.com/Nashi1436/PythonLessonTask_django_web)[←](https://www.notion.so/PythonDjango-c64625cb85d349dcb71b4557d950f415?pvs=21)

[文档更新地址←](https://www.notion.so/PythonDjango-c64625cb85d349dcb71b4557d950f415?pvs=21)

[预览地址](http://121.36.46.222/homepage/)[←](https://www.notion.so/PythonDjango-c64625cb85d349dcb71b4557d950f415?pvs=21)[(已设置为service服务)(2024.1.22后服务器关闭)](http://121.36.46.222/homepage/)

[AI实践←](https://www.notion.so/AI-1a38a869df7d4052aec8f448b1ce5db0?pvs=21)

## **项目描述**

---

基于`django` , `bootstrap3` , `html` , `css` ,  `jQuery` , `Mysql` , `orm`开发的: 

`青藏高原环境监测站数据管理系统` 

本地或服务器部署 浏览器访问使用

### **功能简述**

- 使用`mysql`数据库
- 数据增删查改功能
- 对管理员 用户 部门 监测站 采集信息 的支持
- 数据列表显示分页
- 数据`echart`可视化
- 地图网点定位
- 一键采集所有监测站网点信息
- 访客访问的支持，只能查看数据，修改数据跳转登录
- 数据修改采用`bootstrap3`的form表单修改功能
- 监测站支持图片项， 带有文件上传功能
- `middleware`中间层auth代理，控制访客访问
- `Cookiehe`和`Session`
- 登录验证码
- 时间选择组件
- 用户的所属部门与部门关联
- 跳转主页
- 错误信息支持
- 修改数据不合法保留已输入数据
- excel form上传（前端不可见）
- 调用资源本地化
- 内部密码安全加密
- 对手机端适配
- 使用`django.db.models`自动数据配置
- 各个界面之间关联
- 代码内部注释
- `python脚本`自动创建数据表数据库，初始化网站root管理员
- `docker`  一键部署跨系统支持

### 待实现

- 文件管理 文件预览
- 对小窗的更好适配

## **部署|配置|访问**

---

### 前置推荐环境

```jsx
Python version  3.10.10 
Docker version 24.0.7
Docker Compose version v2.23.3-desktop.2
```

### 手动部署1

安装环境

```jsx
pip install -r requirements.txt
```

在项目根目录下运行`Pre_work/pre_run.py`脚本

自动创建数据库数据表添加网站管理员 ,具体查看调试信息和代码内注释 

默认网站管理员账号：`root`   密码：`qweqwe`

```jsx
python Pre_work/pre_run.py
```

成功如下：

![AD8[0%NSOF~3]BFV301L9B.png](README.assets/AD80NSOF3BFV301L9B.png)

运行

```python
python manage.py runserver
```

### 手动部署2

安装环境 JavaScript Copy Caption pip install -r requirements.txt 

```jsx
安装环境 JavaScript Copy Caption pip install -r requirements.txt 
```

手动创建数据库

修改框中数据库配置

![R15B25919FXEZL5C](./README.assets/R15B25919FXEZL5C.png)

初始化数据库

```jsx
python manage.py makemigrations
python manage.py migrate
```

数据库中手动添加网站管理员在admin表单下

（注意插入的密码为下面目录`md5`函数加密后的字符串)

![ALMRCTHH6Q~V2ZPWMNN{604.png](README.assets/ALMRCTHH6QV2ZPWMNN604.png)

运行

```python
python manage.py runserver
```

### Docker一键部署：

根目录下输入下面指令一键部署

```jsx
docker-compose up --build
```

### **配置**

<代补充>

### **访问**

浏览器访问对应ip端口号进入网站主页

本地访问地址 `[http://localhost:8000/](http://localhost:8000/)`

## **系统总体设计**

---

### **架构**

前端：`html` , `css` , `js` , `bootstrap3`

后端：`django` ,`python` , `xshell`

数据库：`mysql`

### 主要文件逻辑

![DGSU2815UY2I_YINQU3_tmb](./README.assets/DGSU2815UY2I_YINQU3_tmb.png)

### 网络浏览逻辑

![N`Y$Y_6@6KW8ZK@W{QI7NJN_tmb.png](README.assets/NYY_66KW8ZKWQI7NJN_tmb.png)

### 功能逻辑

![DYTGPITP2BLOR3AFY_tmb](./README.assets/DYTGPITP2BLOR3AFY_tmb.png)

### 各模块数据处理逻辑

![HODFR_F_PMHQ9A9LWTOGC_tmb](./README.assets/HODFR_F_PMHQ9A9LWTOGC_tmb.png)

### 文件树目录

```jsx
DJANGO
│  docker-compose.yml      # 用于定义和运行多容器 Docker 应用程序的 Docker Compose 配置文件
│  Dockerfile              # 构建项目 Docker 镜像的指令文件
│  entrypoint.sh           # Docker 容器启动时执行的 Shell 脚本
│  manage.py               # Django 的用于管理任务的命令行工具
│  Monaco.ttf              # 字体文件
│  README.assets.md               # 包含项目信息的 Markdown 文件
│  requirements.txt        # 项目所需的 Python 依赖列表
│  update.md               # 关于项目更新的文档或笔记
│  
├─.idea                    # JetBrains IDE 设置的配置目录
│
├─app01                    # Django 应用目录
│  │  admin.py             # Django 管理界面的配置文件
│  │  apps.py              # Django 应用的配置文件
│  │  models.py            # 定义 Django 模型（数据库表）
│  │  tests.py             # 包含应用的测试用例
│  │  __init__.py          # 表明该目录是一个 Python 包
│  │
│  ├─middleware            # 自定义中间件组件
│  │  │  auth.py           # 认证中间件
│  │  │
│  │  └─__pycache__        # 编译后的 Python 文件，用于加速加载
│  │
│  ├─migrations            # Django 模型的数据库迁移文件
│  │  │
│  │  └─__pycache__
│  │
│  ├─static                # 静态文件目录，如 CSS、JS 和图片
│  │  ├─css                # CSS 文件
│  │  ├─img                # 图片文件
│  │  ├─js                 # JavaScript 文件
│  │  └─plugins            # 额外的插件或库
│  │
│  ├─templates             # 应用的 HTML 模板
│  │      [不同页面和组件的各种 HTML 文件]
│  │
│  ├─utils                 # 实用脚本和辅助函数
│  │  │  [各种 Python 实用工具文件]
│  │  │
│  │  └─__pycache__
│  │
│  ├─views                 # 定义应用的视图（控制4=器）
│  │  │  [不同视图功能的各种 Python 文件]
│  │  │
│  │  └─__pycache__
│  │
│  └─__pycache__
│
├─DJANGO_WEB               # 主项目目录
│  │  asgi.py              # 项目的 ASGI 配置，用于部署
│  │  settings.py          # Django 项目的主设置文件
│  │  urls.py              # Django 项目的 URL 声明
│  │  wsgi.py              # 项目的 WSGI 配置，用于部署
│  │  __init__.py          # 表明该目录是一个 Python 包
│  │
│  └─__pycache__
├─media                    # 媒体文件目录，如用户上传的文件
│
├─Pre_info                 # 额外的目录，可能用于预配置或信息
│      info.txt            # 文本文件，可能包含信息或笔记
│
└─Pre_work                 # 另一个额外的目录，可能用于准备工作
        pre_run.py         # Python 脚本，可能用于设置或初始处理
```

## **未来规划**

---

- 添加文件管理和文件播放功能
- 提高底层代码的复用性
- 添加更多其他功能

## **开发相关**

---

### **团队成员**

- 组长：连浩鸣
- 成员：袁旭
- 成员：曾志亮

### **角色分配**

- 连浩鸣：整体部分，各部分衔接，文档
- 袁旭：账户部分，云服务器部署，截图
- 曾志亮：地图模块，与采集数据关联，文档

### **开发规划**

12月

11号-17号：相关知识学习

18号：参考搜索

19号-21号：主体部分

22号-23号：细节完善，上服务器

24号：docker配置，文档

…

### **开发实践**

- 配置密码时 数据库手动添加的qweqwe，用的密文也就是登录不进去、
  
- ![1DND6LDN6CBZQO6G](./README.assets/1DND6LDN6CBZQO6G.png)
  
    ```python
    注释掉重定向强进 新建的可以进去
    
    最后发现可能是不小心qweqwe打成qwe了 ，但之前调式代码里用的特判是qweqwe
    ```
    
- 配置环境太花时间了 经常系统还各种不兼容
- 有个cenots服务器版本太低没法跑成功初始化数据库的python脚本
  只能手动添加
  
- 用的上海的时区导致传译出问题调几个小时 USE_TZ得改False
  
    ![0SZEFB44VN6AESH](./README.assets/0SZEFB44VN6AESH.png)
    
- Dockerfile 里面用的创建脚本还不支持全平台
  
    ![31UF76S_W4OFWRC](./README.assets/31UF76S_W4OFWRC.png)
    
- Django项目上云不熟悉
允许访问：`ALLOWED_HOSTS = [‘*’]`
时区：`TIME_ZONE = 'Asia/Shanghai’`

## **联系方式**

---

邮箱：1436177712@qq.com

### **技术支持**

[提交issue](https://github.com/Nashi1436/PythonLessonTask_django_web/issues)

## **界面展示**

---

### 用户登陆模块

![wps33.jpg](README.assets/wps33.jpg)

### 数据统计展示模块

![wps34.jpg](README.assets/wps34.jpg)

### 监测站管理模块

![wps36.jpg](README.assets/wps36.jpg)

![wps20.jpg](README.assets/wps20.jpg)

![wps19.jpg](README.assets/wps19.jpg)

### 数据采集模块（允许分类查询）

![wps4.jpg](README.assets/wps4.jpg)

### 管理员模块

![wps8.jpg](README.assets/wps8.jpg)

### 部门模块

![wps10.jpg](README.assets/wps10.jpg)

### 全图监测站模块

![wps25.jpg](README.assets/wps25.jpg)

![wps26.jpg](README.assets/wps26.jpg)

![wps27.jpg](README.assets/wps27.jpg)

### 页脚

![wps23.jpg](README.assets/wps23.jpg)

其他平台

### 服务器端部署

![wps28.jpg](README.assets/wps28.jpg)

![wps29.jpg](README.assets/wps29.jpg)

![wps39.jpg](README.assets/wps39.jpg)

![wps1.jpg](README.assets/wps1.jpg)

![wps30.jpg](README.assets/wps30.jpg)

![wps40.jpg](README.assets/wps40.jpg)

![wps3.jpg](README.assets/wps3.jpg)

![wps5.jpg](README.assets/wps5.jpg)

### ### 其他设备查看

![JFVQK4FRJVQ_L26HSB_tmb](./README.assets/JFVQK4FRJVQ_L26HSB_tmb.jpg)

![1UVRQ[KL]ZE$WF9M_P7IUI7.jpg](README.assets/1UVRQKLZEWF9M_P7IUI7.jpg)

![JFVQK4FRJVQ_L26HSB_tmb](./README.assets/JFVQK4FRJVQ_L26HSB_tmb.jpg)

![V8C88EZ0CDAI3VFHNO_tmb](./README.assets/V8C88EZ0CDAI3VFHNO_tmb.jpg)

## **底层实现**

---

- 密码加密使用 根目录 [\app01\utils\encrypt.py](https://github.com/Nashi1436/PythonLessonTask_django_web/blob/main/app01/utils/encrypt.py) 下：`md5` 加密，数据库存储加密后密码
- 监测站采集数据使用 根目录 [\app01\utils\station.py](https://github.com/Nashi1436/PythonLessonTask_django_web/blob/main/app01/utils/station.py) 下：`get_station`获取随机数据生成，后续有需要可改为pa'qv对应监测站数据