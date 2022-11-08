from django.urls import include, path, reverse
from rest_framework import routers

from character import views

router = routers.SimpleRouter()

router.register(r'', views.CharacterViewSet)
router.register(r'missions', views.MissionViewSet, basename='missions')
router.register(r'arena', views.ArenaViewSet, basename='arena')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
