from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView

from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='blog-home'), # localhost:8000/
    # path('', PostListView.as_view(), name='blog-home'), # CBV homepage > localhost:8000/
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), # localhost:8000/post/1
    path('post/new/', PostCreateView.as_view(), name='post-create'), # localhost:8000/post/new/
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'), # localhost:8000/post/1/update/
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), # localhost:8000/post/1/delete/
    path('about/', views.about, name='blog-about'), # localhost:8000/about/
    path('contact/', views.contact, name='blog-contact'), # localhost:8000/contact/
    path('projects/', views.projects, name='blog-projects'),
    path('post/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('api/', views.post_api_list, name='post_api_list'),
]   

urlpatterns = format_suffix_patterns(urlpatterns)