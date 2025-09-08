from django.contrib.auth import views as auth_views
from django.urls import path, re_path, reverse_lazy

from .views import (
    UserPasswordChangeDoneView, UserPasswordChangeView, user_login,
    user_logout, user_profile)

urlpatterns = [
    re_path(r'login', user_login, name='login'),
    re_path(r'logout', user_logout, name='logout'),
    re_path(r'profile', user_profile, name='user-profile'),
]

# PASSWORD CHANGE
urlpatterns += [
    path('password-change/', UserPasswordChangeView.as_view(), name='password-change'),
    path('password-change-done/', UserPasswordChangeDoneView.as_view(),
         name='password-change-done'),
]

# PASSWORD RESET
urlpatterns += [
    re_path(
        r'^password-reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='trainman/password_reset.html',
            email_template_name='trainman/password_reset_email.html',
            success_url='/trainman/password-reset/done/'
        ),
        name='password-reset'
    ),
    re_path(
        r'^password-reset-done/$',
        auth_views.PasswordResetDoneView.as_view(
            template_name='trainman/password_reset_done.html'
        ),
        name='password-reset-done'
    ),
    re_path(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='trainman/password_reset_confirm.html',
            success_url=reverse_lazy('trainman:password-reset-complete')
        ),
        name='password-reset-confirm'
    ),
    re_path(
        r'^reset-done/$',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='trainman/password_reset_complete.html'
        ),
        name='password-reset-complete'
    ),
]
