from django.urls import path, include

app_name = "api"

urlpatterns = [
    path("account/", include("account.urls_api", namespace="account")),
    path("article/", include("article.urls_api", namespace="article")),
]
