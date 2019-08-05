from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers
from django.conf.urls import url

#router = routers.DefaultRouter()
#router.register('api', views.DmUserListView)

urlpatterns = [

    path('', views.homepage, name='homepage'),
    path('login/', views.user_login, name='user_login_input'),
    path('login/', views.user_login, name='login_error'),
    path('login_details/<int:pk>', views.user_details_output, name='login_detail'),
    # path('new_tweet/new/', views.post_tweet, name='post_tweet'),
    path('new_tweet/error/', views.no_user_found, name='no_user_found'),
    path('users/', views.user_list, name='user_list'),
    path('login_details/<int:pk>/delete', views.user_delete, name='user_delete'),
    path('new_tweet/', views.tweet, name='tweet_posted'),
    path('search/', views.tweet_search_form, name='tweet_search_form'),
    path('search_results/', views.search_results, name='search_results'),
    path('dm_user/<int:user_id>', views.dm),
    path('dm_users/', views.dm_list),
    path('dm_Api/', views.dmAPI),
    #path('test_dm/', views.test_dm)
    #path('dm_user_list/', views.postDmUserList, name='postDmUserList'),
    # path('api_test/', include(router.urls)),

]
