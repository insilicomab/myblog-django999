from django.contrib.auth import views
from django.contrib.auth.views import LoginView
from django.urls import path
from . import views
from .views import (
    CategoryDetailView, CategoryListView, IndexView, PostCreateView, PostDeleteView, 
    PostDetailView, PostListView, PostUpdateView,
    SignUpView, UserLoginView, UserLogoutView,
)


app_name = 'blog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('post_create', PostCreateView.as_view(), name='post_create'),
    path('post_detail/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('post_update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('post_delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('post_list', PostListView.as_view(), name='post_list'),
    path('login', UserLoginView.as_view(), name='login'),
    path('logout', UserLogoutView.as_view(), name='logout'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('like/<int:pk>', views.like_add, name='like_add'),
    path('category_list', CategoryListView.as_view(), name='category_list'),
    path('category_detail/<str:name_en>', CategoryDetailView.as_view(), name='category_detail'),
    path('search', views.search, name='search'),
]