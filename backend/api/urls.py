from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (
    TaskViewSet,
    TagViewSet,
    UserView,
)

router_v1 = DefaultRouter()
router_v1.register(r'users', UserView)
router_v1.register(r'tasks', TaskViewSet, basename='tasks')
router_v1.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
