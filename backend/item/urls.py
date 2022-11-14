from django.urls import include, path, reverse
from item import views
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r"shop", views.ShopViewSet, basename="shop")
router.register(r"backpack", views.BackpackViewSet, basename="backpack")


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
]
