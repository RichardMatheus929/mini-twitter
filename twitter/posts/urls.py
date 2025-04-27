from twitter.posts.views import PostView

from django.urls import path

urlpatterns = [
    path('', PostView.as_view()),
]
