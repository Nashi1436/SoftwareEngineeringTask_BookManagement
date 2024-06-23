from django.shortcuts import render, redirect
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination

class BookModelForm(BootStrapModelForm):
    class Meta:
        model = models.Book
        fields = ["book_name", "author", "publisher", "category", "stock_quantity", "borrow_count", "score", "img"]



def book_register(request):
    """ 注册图书 """
    title = "新建图书"
    if request.method == "GET":
        form = BookModelForm()
        return render(request, 'change.html', {'form': form, "title": title})
    form = BookModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect('/api/book/list/')
    
    return render(request, 'change.html', {'form': form, "title": title})

def book_get(request, book_id):
    """ 获取图书 """
    book_record = models.Book.objects.filter(book_id=book_id).first()
    if not book_record:
        return redirect('/api/book/list/')
    title = "编辑图书"
    if request.method == "GET":
        form = BookModelForm(instance=book_record)
        return render(request, 'change.html', {"form": form, "title": title})
    form = BookModelForm(data=request.POST, files=request.FILES, instance=book_record)
    if form.is_valid():
        form.save()
        return redirect('/api/book/list/')
    return render(request, 'change.html', {"form": form, "title": title})


def book_delete(request, book_id):
    """ 删除图书 """

    user_info = request.session.get("info")
    if not user_info:
        return render(request, 'error.html', {"msg": "用户未登录"})

    user_id = user_info.get("id")
    user_role = user_info.get("role")

    try:
        book_record = models.Book.objects.get(book_id=book_id)
        if user_role < 2:
            return render(request, 'error.html', {"msg": "无权限修改此书籍信息"})
    except ObjectDoesNotExist:
        return render(request, 'error.html', {"msg": "书籍不存在"})


    models.Book.objects.filter(book_id=book_id).delete()
    return redirect('/api/book/list/')


def book_change(request, book_id):
    """ 修改图书信息 """

    user_info = request.session.get("info")
    if not user_info:
        return render(request, 'error.html', {"msg": "用户未登录"})

    user_id = user_info.get("id")
    user_role = user_info.get("role")

    try:
        book_record = models.Book.objects.get(book_id=book_id)
        if user_role < 2:
            return render(request, 'error.html', {"msg": "无权限修改此书籍信息"})
    except ObjectDoesNotExist:
        return render(request, 'error.html', {"msg": "书籍不存在"})


    
    title = f"修改图书信息 - {book_record.book_name}"
    if request.method == "GET":
        form = BookModelForm(instance=book_record)
        return render(request, 'change.html', {"form": form, "title": title})

    form = BookModelForm(data=request.POST, files=request.FILES, instance=book_record)
    if form.is_valid():
        form.save()
        return redirect('/api/book/list/')
    return render(request, 'change.html', {"form": form, "title": title})


def book_search(request):
    """ 搜索图书 """
    return book_list(request)


def book_list(request):
    """ 图书列表 """

    search_data = request.GET.get('q', "")
    find_kind = int(request.GET.get('find_kind', 0))

    query = Q()
    if search_data:
        if find_kind == 1:
            query &= Q(book_name__icontains=search_data)
        elif find_kind == 2:
            query &= Q(author__icontains=search_data)
        elif find_kind == 3:
            query &= Q(publisher__icontains=search_data)
        elif find_kind == 4:
            query &= Q(category__icontains=search_data)
        elif find_kind == 5:
            query &= Q(stock_quantity__icontains=search_data)
        elif find_kind == 6:
            query &= Q(borrow_count__icontains=search_data)
        elif find_kind == 7:
            query &= Q(score__icontains=search_data)
        elif find_kind == 8:
            query &= Q(book_id__icontains=search_data)
        else:
            query &= (Q(book_name__icontains=search_data)       |
                      Q(author__icontains=search_data)          |
                      Q(publisher__icontains=search_data)       |
                      Q(category__icontains=search_data)        |
                      Q(stock_quantity__icontains=search_data)  | 
                      Q(borrow_count__icontains=search_data)    |
                      Q(score__icontains=search_data)           |
                      Q(book_id__icontains=search_data))
            


    queryset = models.Book.objects.filter(query)
    page_object = Pagination(request, queryset)

    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        "search_data": search_data,
        "find_kind": find_kind,
    }
    return render(request, 'book_list.html', context)


