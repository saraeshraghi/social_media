from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegister.as_view(), name='user_register'),
    path('login/', views.UserLogin.as_view(), name='user_login'),
    path('logout/', views.UserLogout.as_view(), name='user_logout'),
    path('profile/<int:user_id>', views.UserProfile.as_view(), name='user_profile'),
    path('reset_pass/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('reset_done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('userfollowing/<int:user_id>/', views.UserFollowing.as_view(), name='user_follow'),
    path('userunfollowing/<int:user_id>/', views.UserUnfollow.as_view(), name='user_unfollow'),
    path('edit_user/', views.EditProfileView.as_view(), name='edit_user'),
]