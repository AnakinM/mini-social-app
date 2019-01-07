from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, CreateComment
from . import views

app_name = 'mainview'
urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    #path('posts/', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView, name='post-detail'),
    path('post/<int:pk>/comment/', CreateComment, name='comment-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
]