from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

api_info = openapi.Info(
    title="altfighter RPG Game API",
    default_version="v1",
    description="Welcome to the altfighter RPG Game API, where you can embark on epic adventures, battle fierce monsters, and become a legendary hero. Explore a world of fantasy and magic in this online role-playing game.",
    contact=openapi.Contact(email="support@altfighter.com"),
    license=openapi.License(name="All Rights Reserved"),
)
schema_view = get_schema_view(
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

urlpatterns += [
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("characters/", include("character.urls")),
    path("items/", include("item.urls")),
]
