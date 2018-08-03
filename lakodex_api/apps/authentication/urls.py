from django.conf.urls import url
from rest_auth.views import (
    LoginView,
    LogoutView,
    UserDetailsView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView
)

from rest_auth.registration.views import (
    VerifyEmailView,
    RegisterView,
    # SocialAccountDisconnectView
)

from .views import (
    FacebookConnect,
    FacebookLogin,
    GoogleConnect,
    GoogleLogin,
    SocialAccountListView,
    PasswordCheckView,
    SocialAccountDisconnectView
)

app_name = 'authentication'

urlpatterns = [


    # url(r'^password/reset/$', PasswordResetView.as_view(), name='rest_password_reset'),
    # url(r'^password/reset/confirm/$', PasswordResetConfirmView.as_view(),name='rest_password_reset_confirm'),

    url(r'^password/change/$', PasswordChangeView.as_view(), name='rest_password_change'),
    url(r'^password/check/$', PasswordCheckView, name="rest_password_check"),

    url(r'^signup/$', RegisterView.as_view(), name='rest_register'),
    url(r'^login/$', LoginView.as_view(), name='rest_login'),
    url(r'^logout/$', LogoutView.as_view(), name='rest_logout'),
    url(r'^$', UserDetailsView.as_view(), name='rest_user_details'),

    url(r'^facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^facebook/connect/$', FacebookConnect.as_view(), name='fb_connect'),

    url(r'^google/$', GoogleLogin.as_view(), name='google_login'),
    url(r'^google/connect/$', GoogleConnect.as_view(), name='google_connect'),


    url(r'^socialaccounts/$', SocialAccountListView.as_view(), name='social_account_list'),
    url(r'^socialaccounts/(?P<pk>\d+)/disconnect/$', SocialAccountDisconnectView.as_view(), name='social_account_disconnect')
]
