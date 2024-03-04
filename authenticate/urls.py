from django.urls import path
from .views import RegisterViews, UpdateUserView, VerifyView, LoginView, UserView, LogoutView, ResendOTPView
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', RegisterViews.as_view(), name='register'),
    path('update/', UpdateUserView.as_view(), name='update-user'),
    path('verify/<str:otp>/', VerifyView.as_view(), name='verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserView.as_view(), name='user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    path('reset_password/', auth_views.PasswordResetView.as_view(),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
