from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'login', views.user_login, name='login'),
    url(r'logout', views.user_logout, name='logout'),
    url(r'profile', views.user_profile, name='user-profile'),
]

# PASSWORD CHANGE
urlpatterns += [
    url(r'password-change', views.user_password_change, name='password-change'),
    url(r'password-change-done', views.user_password_change_done, name='password-change-done'),
]

# PASSWORD RESET
urlpatterns += [
    url(
        regex=r'^password-reset/$',
        view=auth_views.password_reset,
        kwargs={
            'template_name': 'trainman/password_reset.html',
            'email_template_name': 'trainman/password_reset_email.html',
            'post_reset_redirect': 'trainman:password-reset-done'
        },
        name='password-reset'
    ),
    url(
        regex=r'^password-reset-done$',
        view=auth_views.password_reset_done,
        kwargs={
            'template_name': 'trainman/password_reset_done.html'
        },
        name='password-reset-done'
    ),
    url(
        regex=r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        view=auth_views.password_reset_confirm,
        kwargs={
            'template_name': 'trainman/password_reset_confirm.html',
            'post_reset_redirect': 'trainman:password-reset-complete'
        },
        name='password-reset-confirm'
    ),
    url(
        regex=r'^reset-done/$',
        view=auth_views.password_reset_complete,
        kwargs={
            'template_name': 'trainman/password_reset_complete.html'
        },
        name='password-reset-complete'
    ),
]
