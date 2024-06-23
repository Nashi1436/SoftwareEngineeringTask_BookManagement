from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination
from django.db.models import Q


class BorrowRecordModelForm(BootStrapModelForm):
    class Meta:
        model = models.BorrowRecord
        fields = "__all__"

def borrow_in_borrow(request, book_id):
    """ Handles the book borrowing process. """
    if request.method == "GET":
        user_info = request.session.get("info")
        if not user_info:
            return render(request, 'error.html', {"msg": "用户未登录"})

        user_id = user_info.get("id")
        user_role = user_info.get("role")

        if user_role < 1:  # Checks if user role allows borrowing
            return render(request, 'error.html', {"msg": "用户权限不足"})

        try:
            user = models.User.objects.get(user_id=user_id)
            book = models.Book.objects.get(book_id=book_id)
        except ObjectDoesNotExist:
            return render(request, 'error.html', {"msg": "用户或图书不存在"})

        if book.stock_quantity > 0:
            book.stock_quantity -= 1
            book.borrow_count += 1
            book.save()

            borrow_record = models.BorrowRecord(user_id=user, book_id=book)
            borrow_record.save()
            return redirect('/api/borrow/list/')
        else:
            return render(request, 'error.html', {"msg": "库存不足"})
    return render(request, 'error.html', {"msg": "无效的请求方法"})

def borrow_out_borrow(request, record_id):
    """ Handles the book return process. """
    if request.method == "GET":
        user_info = request.session.get("info")
        if not user_info:
            return render(request, 'error.html', {"msg": "用户未登录"})

        user_id = user_info.get("id")
        user_role = user_info.get("role")

        try:
            borrow_record = models.BorrowRecord.objects.get(record_id=record_id)
            print(borrow_record.user_id.user_id )
            print(user_id)
            print(user_role)
            if borrow_record.user_id.user_id != user_id and user_role < 2:
                return render(request, 'error.html', {"msg": "用户无权限归还此书"})
        except ObjectDoesNotExist:
            return render(request, 'error.html', {"msg": "借阅记录不存在"})

        if borrow_record.status == 1:
            borrow_record.status = 2
            borrow_record.return_date = timezone.now()
            borrow_record.save()

            book = borrow_record.book_id
            book.stock_quantity += 1
            book.save()
            return redirect('/api/borrow/list/')
        else:
            return render(request, 'error.html', {"msg": "该书籍未处于借阅状态"})
    return render(request, 'error.html', {"msg": "无效的请求方法"})





def borrow_delete(request, record_id):
    """ Deletes a borrowing record. """

    user_info = request.session.get("info")
    if not user_info:
        return render(request, 'error.html', {"msg": "用户未登录"})

    user_id = user_info.get("id")
    user_role = user_info.get("role")
    borrow_record = models.BorrowRecord.objects.get(record_id=record_id)

    if borrow_record.user_id.user_id != user_id and user_role < 2:
        return render(request, 'error.html', {"msg": "用户无权限删除此借阅记录"})
    
    models.BorrowRecord.objects.filter(record_id=record_id).delete()
    return redirect('/api/borrow/list/')




def borrow_change(request, record_id):
    """ Modifies an existing borrowing record. """

    user_info = request.session.get("info")
    if not user_info:
        return render(request, 'error.html', {"msg": "用户未登录"})

    user_id = user_info.get("id")
    user_role = user_info.get("role")

    try:
        borrow_record = models.BorrowRecord.objects.get(record_id=record_id)
        if user_role < 2:
            return render(request, 'error.html', {"msg": "用户无权限修改记录"})
    except ObjectDoesNotExist:
        return render(request, 'error.html', {"msg": "借阅记录不存在"})
    
    if request.method == "GET":
        form = BorrowRecordModelForm(instance=borrow_record)
        return render(request, 'change.html', {"form": form, "title": f"修改借阅记录 - {borrow_record.user_id.username} - {borrow_record.book_id.book_name}"})

    elif request.method == "POST":
        form = BorrowRecordModelForm(data=request.POST, instance=borrow_record)
        if form.is_valid():
            form.save()
            return redirect('/api/borrow/list/')
        else:
            return render(request, 'change.html', {"form": form, "title": f"修改借阅记录 - {borrow_record.user_id.username} - {borrow_record.book_id.book_name}"})



def borrow_get(request, record_id):
    """ Retrieves a specific borrowing record. """
    try:
        borrow_record = models.BorrowRecord.objects.get(record_id=record_id)
        data = {
            "record_id": borrow_record.record_id,
            "user": borrow_record.user_id.username,
            "book": borrow_record.book_id.book_name,
            "borrow_date": borrow_record.borrow_date,
            "return_date": borrow_record.return_date,
            "status": borrow_record.get_status_display()
        }
        return JsonResponse({"status": "success", "data": data})
    except ObjectDoesNotExist:
        return render(request, 'error.html', {"msg": "借阅记录不存在"})


def borrow_list(request):
    """ Lists all borrowing records, possibly filtered by user search. """
    search_data = request.GET.get('q', "")
    status_filter = request.GET.get('status', "")
    find_kind = int(request.GET.get('find_kind', 0))

    query = Q()
    if search_data:
        if find_kind == 1:
            query &= Q(user_id__username__icontains=search_data)
        elif find_kind == 2:
            query &= Q(book_id__book_name__icontains=search_data)
        else:
            query &= (Q(user_id__username__icontains=search_data) | 
                      Q(book_id__book_name__icontains=search_data))

    if status_filter:
        query &= Q(status=status_filter)

    queryset = models.BorrowRecord.objects.filter(query)
    page_object = Pagination(request, queryset)

    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        "search_data": search_data,
        "find_kind": find_kind,
        "status_filter": status_filter
    }
    return render(request, 'borrow_list.html', context)

