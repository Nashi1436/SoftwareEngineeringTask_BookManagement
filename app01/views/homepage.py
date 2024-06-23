from django.shortcuts import render
from app01 import models

def homepage_homepage(request):
    """ 首页视图 """
    recommended_books = models.Book.objects.order_by('-score')[:6]  # 按评分推荐前 6 本书
    latest_borrows = models.BorrowRecord.objects.order_by('-borrow_date')[:6]  # 最新借阅记录前 6 条
    user_info = request.session.get("info", {})
    if user_info:
        user_id = user_info.get("id")
        user = models.User.objects.get(user_id=user_id)
        user_reviews = models.ScoreRecord.objects.filter(user_id=user_id)
    else:
        user = None
        user_reviews = []

    context = {
        'recommended_books': recommended_books,
        'latest_borrows': latest_borrows,
        'user': user,
        'user_reviews': user_reviews,
    }
    return render(request, 'homepage.html', context)
