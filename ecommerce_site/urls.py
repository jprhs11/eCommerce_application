from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from store import views as store_views

urlpatterns = [
    # Authentication & Registration
    path('register/', store_views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Password Reset URLs
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),

    # Admin and Main Application URLs
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
]
