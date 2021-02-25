from django.urls import path, include

app_name = "api"

urlpatterns = [
    path("account/", include("account.urls", namespace="account")),
    path("article/", include("article.urls", namespace="article")),
]
