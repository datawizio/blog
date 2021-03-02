from django.db.models import Count
from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.


class PostList(ListView):
    queryset = Post.objects.publish().annotate(like_count=Count("likes"))
    template_name = "index.html"


class PostDetail(DetailView):
    model = Post
    template_name = "post_detail.html"
