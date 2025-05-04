from twitter.accounts.views import Signin, Signup, UsersViewSet
from rest_framework.routers import DefaultRouter

from django.urls import path, include

router = DefaultRouter()
router.register(r'', UsersViewSet, basename='')

urlpatterns = [
    path('', include(router.urls)),
    path('signin', Signin.as_view()),
    path('signup', Signup.as_view()),
]
