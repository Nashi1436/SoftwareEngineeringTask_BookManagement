from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count

from app01 import models

def chart_list(request):
    """ 数据统计页面 """
    return render(request, 'chart_list.html')


def chart_bar(request):
    """ 构造柱状图的数据 """

    # 从数据库中获取City模型的数据
    cities = models.City.objects.all()
    legend = ["终端数量"]
    x_axis = [city.name for city in cities]
    series_list = [
        {
            "name": '终端数量',
            "type": 'bar',
            "data": [city.count for city in cities]
        }
    ]

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)






def chart_pie(request):
    """ 构造饼图的数据 """

    # 使用annotate和Count来获取每个来源监测站的采集信息次数
    data = Catch.objects.values('name').annotate(count=Count('name')).order_by('-count')

    # 构造饼图数据
    db_data_list = [{"value": entry['count'], "name": entry['name']} for entry in data]

    result = {
        "status": True,
        "data": db_data_list
    }
    return JsonResponse(result)



from django.http import JsonResponse
from django.db.models.functions import ExtractMonth
from django.db.models import Avg
from app01.models import Catch

def chart_line(request):
    # 按月份计算每项数据的平均值
    monthly_avg = Catch.objects.annotate(month=ExtractMonth('create_time')).values('month').annotate(
        avg_wendu=Avg('wendu'),
        avg_fengsu=Avg('fengsu'),
        avg_shidu=Avg('shidu'),
        avg_pm25=Avg('pm25')
    ).order_by('month')

    # 准备数据以符合 ECharts 格式
    data_wendu = [0] * 12
    data_fengsu = [0] * 12
    data_shidu = [0] * 12
    data_pm25 = [0] * 12

    # 填充数据
    for entry in monthly_avg:
        print(entry['month'])
        month_index = entry['month'] - 1
        data_wendu[month_index] = entry['avg_wendu']
        data_fengsu[month_index] = entry['avg_fengsu']
        data_shidu[month_index] = entry['avg_shidu']
        data_pm25[month_index] = entry['avg_pm25']

    # 设置图表的 legend 和 series
    legend = ["平均温度", "平均风速", "平均湿度", "平均PM2.5"]
    series_list = [
        {"name": "平均温度", "type": 'line', "data": data_wendu},
        {"name": "平均风速", "type": 'line', "data": data_fengsu},
        {"name": "平均湿度", "type": 'line', "data": data_shidu},
        {"name": "平均PM2.5", "type": 'line', "data": data_pm25}
    ]
    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def highcharts(request):
    """ highcharts示例 """

    return render(request, 'highcharts.html')


from django.forms import ModelForm, Form
from django import forms
from app01 import models


# class TTModelForm(Form):
#     name = forms.CharField(label="用户名")
#     ff = forms.FileField(label="文件")
#
#
# def tt(request):
#     if request.method == "GET":
#         form = TTModelForm()
#         return render(request, 'change.html', {"form": form})
#     form = TTModelForm(data=request.POST, files=request.FILES)
#     if form.is_valid():
#         print(form.cleaned_data)
#     return render(request, 'change.html', {"form": form})

class TTModelForm(ModelForm):
    class Meta:
        model = models.XX
        fields = "__all__"


def tt(request):
    instance = models.XX.objects.all().first()
    if request.method == "GET":
        form = TTModelForm(instance=instance)
        return render(request, 'tt.html', {"form": form})
    form = TTModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
    return render(request, 'tt.html', {"form": form})
