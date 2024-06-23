from django.shortcuts import render, redirect

from app01 import models
from app01.utils.pagination import Pagination

from django import forms
from django.core.exceptions import ValidationError
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination


class UserModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.User
        fields = ["username", "password", "confirm_password", "email", "phone"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        # 返回什么，此字段以后保存到数据库就是什么。
        return confirm



# class UserEditModelForm(BootStrapModelForm):
#     class Meta:
#         model = models.User
#         fields = ['username']


class UserResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.User
        fields = ['password', 'confirm_password']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)

        # 去数据库校验当前密码和新输入的密码是否一致
        exists = models.User.objects.filter(user_id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("不能与以前的密码相同")
        
        return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        # 返回什么，此字段以后保存到数据库就是什么。
        return confirm



def user_register(request):
    """ 注册用户 """
    title = "新建用户"
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'change.html', {'form': form, "title": title})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/api/user/list/')
    
    return render(request, 'change.html', {'form': form, "title": title})


def user_get(request, user_id):
    """ 获取用户 """
    user_record = models.User.objects.filter(user_id=user_id).first()
    if not user_record:
        return redirect('/api/user/list/')
    title = "编辑用户"
    if request.method == "GET":
        form = UserModelForm(instance=user_record)
        return render(request, 'change.html', {"form": form, "title": title})
    form = UserModelForm(data=request.POST, instance=user_record)
    if form.is_valid():
        form.save()
        return redirect('/api/user/list/')
    return render(request, 'change.html', {"form": form, "title": title})


def user_delete(request, user_id):
    """ 删除用户 """

    user_info = request.session.get("info")
    if not user_info:
        return render(request, 'error.html', {"msg": "用户未登录"})

    user_id = user_info.get("id")
    user_role = user_info.get("role")

    try:
        user_record = models.User.objects.get(user_id=user_id)
        if user_record.user_id != user_id or user_role < 2:
            return render(request, 'error.html', {"msg": "无权限删除此用户"})
    except ObjectDoesNotExist:
        return render(request, 'error.html', {"msg": "用户不存在"})


    models.User.objects.filter(user_id=user_id).delete()
    return redirect('/api/user/list/')


def user_change(request, user_id):
    """ 修改用户信息 """


    user_info = request.session.get("info")
    if not user_info:
        return render(request, 'error.html', {"msg": "用户未登录"})

    user_id = user_info.get("id")
    user_role = user_info.get("role")

    try:
        user_record = models.User.objects.get(user_id=user_id)
        if user_record.user_id != user_id or user_role < 2:
            return render(request, 'error.html', {"msg": "无权限修改此用户信息"})
    except ObjectDoesNotExist:
        return render(request, 'error.html', {"msg": "用户不存在"})
    

    
    title = f"修改用户信息 - {user_record.username}"
    if request.method == "GET":
        form = UserModelForm(instance=user_record)
        # form.fields['password'].initial = ''  # 确保密码字段初始化为空
        print(form.fields['password'].initial)
        return render(request, 'change.html', {"form": form, "title": title})

    form = UserModelForm(data=request.POST, instance=user_record)
    if form.is_valid():
        form.save()
        return redirect('/api/user/list/')
    return render(request, 'change.html', {"form": form, "title": title})


def user_reset(request, user_id):
    """ 重置密码 """

    
    user_info = request.session.get("info")
    if not user_info:
        return render(request, 'error.html', {"msg": "用户未登录"})

    user_id = user_info.get("id")
    user_role = user_info.get("role")

    try:
        user_record = models.User.objects.get(user_id=user_id)
        if user_record.user_id != user_id or user_role < 2:
            return render(request, 'error.html', {"msg": "无权限修改此用户密码"})
    except ObjectDoesNotExist:
        return render(request, 'error.html', {"msg": "用户不存在"})
    
    title = f"重置密码 - {user_record.username}"


    if request.method == "GET":
        form = UserResetModelForm()
        return render(request, 'change.html', {"form": form, "title": title})
    
    form = UserResetModelForm(data=request.POST, instance=user_record)
    if form.is_valid():
        form.save()
        return redirect('/api/user/list/')
    return render(request, 'change.html', {"form": form, "title": title})



def user_list(request):
    """ 用户列表 """
    

    search_data = request.GET.get('q', "")
    role_filter = request.GET.get('role', "")
    find_kind = int(request.GET.get('find_kind', 0))

    query = Q()
    if search_data:
        if find_kind == 1:
            query &= Q(username__icontains=search_data)
        elif find_kind == 2:
            query &= Q(email__icontains=search_data)
        elif find_kind == 3:
            query &= Q(phone__icontains=search_data)
        elif find_kind == 4:
            query &= Q(registration_date__icontains=search_data)
        elif find_kind == 5:
            query &= Q(user_id__icontains=search_data)
        else:
            query &= (Q(username__icontains=search_data) |
                      Q(email__icontains=search_data)    |
                      Q(phone__icontains=search_data)    | 
                      Q(user_id__icontains=search_data)  |
                      Q(registration_date__icontains=search_data) )
            
    if role_filter:
        query &= Q(role=role_filter)

    queryset = models.User.objects.filter(query)
    page_object = Pagination(request, queryset)

    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        "search_data": search_data,
        "find_kind": find_kind,
        "role_filter": role_filter
    }
    return render(request, 'user_list.html', context)