from django.urls import path, include
from . import views

app_name = 'article'

urlpatterns = [
    path('article-list/', views.article_list, name='article_list'),
    path('', views.test404, name='test404'),
]