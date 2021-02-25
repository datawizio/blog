from rest_framework_extensions.routers import ExtendedDefaultRouter

from . import viewsets as article_viewsets

app_name = "article"
router = ExtendedDefaultRouter()

posts_router = router.register(r"posts", article_viewsets.PostModelViewSet, basename="posts")
posts_router.register(
    r"comments",
    article_viewsets.CommentModelViewSet,
    basename="comments",
    parents_query_lookups=["post_id"]
)

urlpatterns = router.urls
