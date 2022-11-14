from allauth.account.views import confirm_email
from django.urls import include, path, re_path

from .views import FacebookLogin, GoogleLogin

urlpatterns = [
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path("account/", include("allauth.urls")),
    re_path(
        r"accounts-rest/registration/account-confirm-email/(?P<key>.+)/$",
        confirm_email,
        name="account_confirm_email",
    ),
    path("dj-rest-auth/facebook/", FacebookLogin.as_view(), name="fb_login"),
    path("dj-rest-auth/google/", GoogleLogin.as_view(), name="google_login"),
]
