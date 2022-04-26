from django.urls import include, path
from rest_framework import routers
from character import views
from django.urls import reverse
router = routers.SimpleRouter()

router.register(r'statss', views.StatsViewSet)
router.register(r'characters', views.CharacterViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'items', views.ItemViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]