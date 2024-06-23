from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination
from django.db.models import Avg
from django.db.models import Q


class RatingAndReviewModelForm(BootStrapModelForm):
    class Meta:
        model = models.ScoreRecord
        fields = ['rating', 'review']

def ratingandreview_register(request, book_id):
    """ 注册评分和评论 """
    if request.method == "POST":
        user_info = request.session.get("info")
        if not user_info:
            return render(request, 'error.html', {"msg": "用户未登录"})

        user_id = user_info.get("id")
        
        try:
            user = models.User.objects.get(user_id=user_id)
            book = models.Book.objects.get(book_id=book_id)
        except ObjectDoesNotExist:
            return render(request, 'error.html', {"msg": "用户或图书不存在"})

        form = RatingAndReviewModelForm(data=request.POST)
        if form.is_valid():
            rating_and_review = form.save(commit=False)
            rating_and_review.user_id = user
            rating_and_review.book_id = book
            rating_and_review.save()
            
            # 更新书籍评分
            book.score = models.ScoreRecord.objects.filter(book_id=book).aggregate(Avg('rating'))['rating__avg']
            book.save()

            return redirect('/api/ratingandreview/list/')
        return render(request, 'change.html', {"form": form, "title": "提交评分和评论"})
    
    form = RatingAndReviewModelForm()
    return render(request, 'change.html', {"form": form, "title": "提交评分和评论"})

def ratingandreview_delete(request, record_id):
    """ 删除评分和评论 """

    user_info = request.session.get("info")
    if not user_info:
        return render(request, 'error.html', {"msg": "用户未登录"})


    user_id = user_info.get("id")
    user_role = user_info.get("role")


    try:
        ratingandreview_record = models.ScoreRecord.objects.get(record_id=record_id)
        if ratingandreview_record.user_id.user_id != user_id and user_role < 2:
            return render(request, 'error.html', {"msg": "用户无权限删除此评分评论"})
    except ObjectDoesNotExist:
        return render(request, 'error.html', {"msg": "借阅记录不存在"})

    models.ScoreRecord.objects.filter(record_id=record_id).delete()
    return redirect('/api/ratingandreview/list/')
    

def ratingandreview_change(request, record_id):
    """ 修改评分和评论 """

    user_info = request.session.get("info")
    if not user_info:
        return render(request, 'error.html', {"msg": "用户未登录"})

    user_id = user_info.get("id")
    user_role = user_info.get("role")


    try:
        ratingandreview_record = models.ScoreRecord.objects.get(record_id=record_id)
        print(ratingandreview_record.user_id.user_id)
        print(user_id)
        print(user_role)
        if ratingandreview_record.user_id.user_id != user_id and user_role < 2:
            return render(request, 'error.html', {"msg": "用户无权限修改此评分评论"})
    except ObjectDoesNotExist:
        return render(request, 'error.html', {"msg": "借阅记录不存在"})

    
    title = f"修改评分和评论 - {ratingandreview_record.user_id.username} - {ratingandreview_record.book_id.book_name}"
    if request.method == "GET":
        form = RatingAndReviewModelForm(instance=ratingandreview_record)
        return render(request, 'change.html', {"form": form, "title": title})

    
    elif request.method == "POST":
        form = RatingAndReviewModelForm(data=request.POST, instance=ratingandreview_record)
        if form.is_valid():
            form.save()
            # 更新书籍评分
            book = ratingandreview_record.book_id
            book.score = models.ScoreRecord.objects.filter(book_id=book).aggregate(Avg('rating'))['rating__avg']
            book.save()

            return redirect('/api/ratingandreview/list/')
        return render(request, 'change.html', {"form": form, "title": title})


def ratingandreview_get(request, record_id):
    """ 获取评分和评论 """
    try:
        rating_and_review = models.ScoreRecord.objects.get(record_id=record_id)
    except ObjectDoesNotExist:
        return render(request, 'error.html', {"msg": "评分和评论记录不存在"})

    data = {
        "record_id": rating_and_review.record_id,
        "user": rating_and_review.user_id.username,
        "book": rating_and_review.book_id.book_name,
        "rating": rating_and_review.rating,
        "review": rating_and_review.review,
    }
    return JsonResponse({"status": "success", "data": data})

def ratingandreview_list(request):
    """ 评分和评论记录列表 """
    search_data = request.GET.get('q', "")
    find_kind = int(request.GET.get('find_kind', 0))


    query = Q()
    if search_data:
        if find_kind == 1:
            query &= Q(user_id__username__icontains=search_data)
        elif find_kind == 2:
            query &= Q(book_id__book_name__icontains=search_data)
        elif find_kind == 3:
            query &= Q(review__icontains=search_data)
        else:
            query &= (Q(user_id__username__icontains=search_data) | 
                      Q(book_id__book_name__icontains=search_data)|
                      Q(review__icontains=search_data))


    queryset = models.ScoreRecord.objects.filter(query)
    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        "search_data": search_data,
        "find_kind": find_kind,
    }
    return render(request, 'ratingandreview_list.html', context)

