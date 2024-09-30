from django.urls import path
from . import controller_news

urlpatterns = [
    path('all/', controller_news.get_all_news, name='get_all_news'),
    path('news/<int:news_id>/', controller_news.get_one_news, name='get_one_news'),
    path('news/create/', controller_news.create_news, name='create_news'),
    path('news/update/<int:news_id>/', controller_news.update_news, name='update_news'),
    path('news/delete/<int:news_id>/', controller_news.delete_news, name='delete_news'),
]
