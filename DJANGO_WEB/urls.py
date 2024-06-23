"""DJANGO_WEB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

# from app01.views import depart, user, admin, account,  chart, upload, city, catch
from app01.views import homepage,account
from app01.views import user, book, borrow, recommendations, ratingandreview

urlpatterns = [
    # path('admin/', admin.site.urls),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    
    #主页
    path('homepage/',homepage.homepage_homepage),
    path('', homepage.homepage_homepage),


    # 登录
    path('login/', account.login),
    path('logout/', account.logout),
    path('register/', account.logout),
    path('image/code/', account.image_code),




    # 用户管理模块接口
    # path('api/user/login/', user.user_login),
    # path('api/user/logout/', user.user_logout),
    path('api/user/register/', user.user_register),
    path('api/user/get/<int:user_id>/', user.user_get),
    path('api/user/delete/<int:user_id>/', user.user_delete),
    path('api/user/change/<int:user_id>/', user.user_change),
    path('api/user/reset/<int:user_id>/', user.user_reset),
    path('api/user/list/', user.user_list),
    


    # # 图书管理模块接口
    path('api/book/register/', book.book_register),
    path('api/book/get/<int:book_id>/', book.book_get),
    path('api/book/delete/<int:book_id>/', book.book_delete),
    path('api/book/change/<int:book_id>/', book.book_change),
    path('api/book/search/', book.book_search),
    path('api/book/list/', book.book_list),
    


    # # 借阅管理模块接口
    

    path('api/borrow/in/<int:book_id>/', borrow.borrow_in_borrow),
    path('api/borrow/out/<int:record_id>/', borrow.borrow_out_borrow),
    path('api/borrow/delete/<int:record_id>/', borrow.borrow_delete),
    path('api/borrow/change/<int:record_id>/', borrow.borrow_change),
    path('api/borrow/get/<int:record_id>/', borrow.borrow_get),
    path('api/borrow/list/', borrow.borrow_list),
    
    

    # 推荐管理模块接口
    path('api/recommendations/push_random/', recommendations.recommendations_push_random),
    path('api/recommendations/push_score/', recommendations.recommendations_push_score),
    path('api/recommendations/push_count/', recommendations.recommendations_push_count),
    


    # 评分评论模块接口

    path('api/ratingandreview/register/<int:book_id>/', ratingandreview.ratingandreview_register),
    path('api/ratingandreview/delete/<int:record_id>/', ratingandreview.ratingandreview_delete),
    path('api/ratingandreview/change/<int:record_id>/', ratingandreview.ratingandreview_change),
    path('api/ratingandreview/get/<int:record_id>/', ratingandreview.ratingandreview_get),
    path('api/ratingandreview/list/', ratingandreview.ratingandreview_list),





















    







    # # 部门管理
    # path('depart/list/', depart.depart_list),
    # path('depart/add/', depart.depart_add),
    # path('depart/<int:nid>/edit/', depart.depart_edit),
    # path('depart/<int:nid>/delete/', depart.depart_delete),
    # path('depart/multi/', depart.depart_multi),



    # # 数据统计
    # path('chart/list/', chart.chart_list),
    # path('chart/bar/', chart.chart_bar),
    # path('chart/pie/', chart.chart_pie),
    # path('chart/line/', chart.chart_line),
    # path('chart/highcharts/', chart.highcharts),

    

    # # 监测站管理
    # path('city/list/', city.city_list),
    # path('city/add/', city.city_add),
    # path('city/<int:nid>/edit/', city.city_edit),
    # path('city/<int:nid>/delete/', city.city_delete),
    # path('city/<int:nid>/map/', city.city_map),
    # path('city/map/all', city.city_map_all),
    

    # #采集信息
    # path('catch/list/', catch.catch_list),
    # path('catch/add/', catch.catch_add),
    # path('catch/<int:nid>/edit/', catch.catch_edit),
    # path('catch/<int:nid>/delete/', catch.catch_delete),
    # path('catch/<int:nid>/capture/', catch.catch_capture),
    # path('catch/capture/all/', catch.catch_capture_all),


    

    
    
    # 调试
    # path('tt/', chart.tt),

]
