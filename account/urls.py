from rest_framework.routers import DefaultRouter

from . import viewsets as account_viewsets

app_name = "account"
router = DefaultRouter()

router.register(r"users", account_viewsets.UserViewSet, basename="users")

urlpatterns = router.urls
