
from django.shortcuts import render, redirect
from django import forms

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination
from app01.utils.station import get_station

def catch_list(request):

    # 构造搜索
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    # 根据搜索条件去数据库获取
    queryset = models.Catch.objects.filter(**data_dict).order_by('-id')
    # 分页
    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        "search_data": search_data
    }
    return render(request, 'catch_list.html', context)



# class CustomDateInput(forms.DateInput):
#     def __init__(self, **kwargs):
#         kwargs['attrs'] = {'class': 'datepicker'}
#         super().__init__(**kwargs)
# class CustomDateTimeInput(forms.DateTimeInput):
#     def __init__(self, **kwargs):
#         kwargs['attrs'] = {'class': 'datetimepicker'}
#         super().__init__(**kwargs)

class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.Catch
        fields = "__all__"
        widgets = {
            'create_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

def catch_add(request):
    """ 添加采集信息 """
    title = "添加采集信息"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'change.html', {"form": form, 'title': title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/catch/list/")
    return render(request, 'change.html', {"form": form, 'title': title})


def catch_edit(request, nid):
    """ 编辑采集信息 """
    # 对象 / None
    row_object = models.Catch.objects.filter(id=nid).first()
    if not row_object:
        # return render(request, 'error.html', {"msg": "数据不存在"})
        return redirect('/catch/list/')

    title = "编辑采集信息"
    if request.method == "GET":
        form = UpModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})

    form = UpModelForm(data=request.POST, files=request.FILES, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/catch/list/')
    return render(request, 'change.html', {"form": form, "title": title})


def catch_delete(request, nid):
    """ 删除采集信息 """
    models.Catch.objects.filter(id=nid).delete()
    return redirect('/catch/list/')


def catch_capture(request, nid):
    """ 捕获 """
    title = "捕获"
    # 对象 / None
    row_object = models.City.objects.filter(id=nid).first()
    
    if not row_object:
        # return render(request, 'error.html', {"msg": "监测站不存在"})
        return redirect('/city/list/')

    form = UpModelForm(data=get_station(row_object.name), files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/catch/list/")
    return render(request, 'change.html', {"form": form, 'title': title})

def catch_capture_all(request):
    """ 捕获所有 """
    title = "添加采集信息"

    for row_object in models.City.objects.all():
        if not row_object: continue
        form = UpModelForm(data=get_station(row_object.name), files=request.FILES)
        if form.is_valid():
            form.save()
    return redirect("/catch/list/")
    