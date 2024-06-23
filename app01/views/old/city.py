from django.shortcuts import render, redirect
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
import json

from app01.utils.pagination import Pagination

def city_list(request):

    # 构造搜索
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    # 根据搜索条件去数据库获取
    queryset = models.City.objects.filter(**data_dict).order_by('-id')
    # 分页
    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        "search_data": search_data
    }
    return render(request, 'city_list.html', context)

class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.City
        fields = "__all__"


def city_add(request):
    """ 添加检测站 """
    title = "添加监测站"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'upload_form.html', {"form": form, 'title': title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 对于文件：自动保存；
        # 字段 + 上传路径写入到数据库
        form.save()
        return redirect("/city/list/")
    return render(request, 'upload_form.html', {"form": form, 'title': title})


def city_edit(request, nid):
    """ 编辑观测站 """
    # 对象 / None
    row_object = models.City.objects.filter(id=nid).first()
    if not row_object:
        # return render(request, 'error.html', {"msg": "数据不存在"})
        return redirect('/city/list/')

    title = "编辑观测站"
    if request.method == "GET":
        form = UpModelForm(instance=row_object)
        return render(request, 'upload_form.html', {"form": form, "title": title})

    form = UpModelForm(data=request.POST, files=request.FILES, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/city/list/')
    return render(request, 'upload_form.html', {"form": form, "title": title})


def city_delete(request, nid):
    """ 删除观测站 """
    models.City.objects.filter(id=nid).delete()
    return redirect('/city/list/')


def city_map(request, nid):
    """ 定位地图 """
    queryset = models.City.objects.all()
    station = models.City.objects.all().filter(id=nid).first()

     # 构造搜索
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data
        # 根据搜索条件去数据库获取
        queryset = models.City.objects.filter(**data_dict).order_by('-id')
        station = queryset.first()

    return render(request, 'map.html', {'local': station, "queryset": queryset})

def city_map_all(request):
    """ 定位地图 """
    queryset = models.City.objects.all()
    station = None
    return render(request, 'map.html', {'local': station, "queryset": queryset})