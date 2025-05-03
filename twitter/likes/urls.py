from django.urls import path, include
from rest_framework.routers import DefaultRouter
from twitter.likes.views import LikeViewSet

router = DefaultRouter()
router.register(r'', LikeViewSet, basename='likes')

urlpatterns = [
    path('', include(router.urls)),
]