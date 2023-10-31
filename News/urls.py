from django.urls import path
from .views import PostList, PostDetail, PostSearch, NewCreate, NewEdit, NewDelete, ArticleCreate, ArticleEdit, ArticleDelete, subscriptions


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search', PostSearch.as_view()),
    path('news/create/', NewCreate.as_view(), name='new_create'),
    path('news/<int:pk>/edit/', NewEdit.as_view(), name='new_edit'),
    path('news/<int:pk>/delete/', NewDelete.as_view(), name='new_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]