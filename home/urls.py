from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('post/detail/<int:post_id>/<word>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/reply/<int:post_id>/<int:comment_id>/', views.ReplyComment.as_view(), name='add_reply'),
    path('post/delete/<int:post_id>/', views.PostDetail.as_view(), name='post_delete'),
    path('post/create/', views.PostCreate.as_view(), name='post_create'),
    path('post/update/<int:post_id>/', views.PostUpdate.as_view(), name='post_update'),
    path('post/like/<int:post_id>/', views.PostLike.as_view(), name='post_like'),
]