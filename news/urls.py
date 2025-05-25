from django.urls import path
from .views import NewsItemCreateView, NewsItemListCreateView, NewsItemDeleteView

urlpatterns = [
    path('news/create/', NewsItemCreateView.as_view(), name='news-create'),
    path('news/', NewsItemListCreateView.as_view(), name='news-list-create'),
    path('news/<int:pk>/delete/', NewsItemDeleteView.as_view(), name='newsitem-delete')
]
