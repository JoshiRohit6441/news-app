from django.urls import path, include
from .views import NewsView, AllNews, CategoryView


urlpatterns = [
    path('category/', CategoryView.as_view(), name='category'),
    path('news/', NewsView.as_view(), name='news'),
    path('news/<int:id>/', NewsView.as_view(), name='news-id'),
    path('allNews/', AllNews.as_view(), name='all-news'),
]
