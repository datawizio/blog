from django.urls import path

from .views import PostList, PostDetail, Index


urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("blog/", PostList.as_view(), name="blog"),
    path("blog/<slug:slug>/", PostDetail.as_view(), name="post_detail"),
]
