
from django.shortcuts import render, redirect
from django import forms

from app01.utils.bootstrap import BootStrapModelForm
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm

class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.UserInfo
        fields = "__all__"
        widgets = {
            'create_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

def user_list(request):
    """ 用户管理 """

    # 构造搜索
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    # 根据搜索条件去数据库获取
    queryset = models.UserInfo.objects.filter(**data_dict).order_by('-id')
    # 分页
    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        "search_data": search_data
        
    }
    return render(request, 'user_list.html', context)


def user_add(request):
    """ 添加用户 """
    title = "添加用户"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'change.html', {"form": form, 'title': title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, 'change.html', {"form": form, 'title': title})


def user_edit(request, nid):
    """ 编辑用户 """
    row_object = models.UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据（对象）
        form = UserModelForm(instance=row_object)
        return render(request, 'change.html', {'form': form})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要再用户输入以外增加一点值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/user/list/')
    return render(request, 'change.html', {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')
