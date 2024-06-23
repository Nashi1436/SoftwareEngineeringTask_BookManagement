import random
from django.shortcuts import render
from django.http import JsonResponse
from app01 import models
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


from django.shortcuts import render
from app01 import models
from random import sample

def recommendations_push_random(request):
    """ 随机推荐书籍 """
    title = f"推荐书籍--随机推荐"
    books = list(models.Book.objects.all())
    recommended_books = sample(books, min(len(books), 10))  # 随机推荐最多10本书
    return render(request, 'recommendations_list.html', {'books': recommended_books, 'title': title})

def recommendations_push_score(request):
    """ 按评分推荐书籍 """
    title = f"推荐书籍--评分推荐"
    recommended_books = models.Book.objects.all().order_by('-score')[:10]  # 按评分推荐前10本书
    return render(request, 'recommendations_list.html', {'books': recommended_books, 'title': title})

def recommendations_push_count(request):
    """ 按借阅次数推荐书籍 """
    title = f"推荐书籍--订阅推荐"
    recommended_books = models.Book.objects.all().order_by('-borrow_count')[:10]  # 按借阅次数推荐前10本书
    return render(request, 'recommendations_list.html', {'books': recommended_books, 'title': title})

