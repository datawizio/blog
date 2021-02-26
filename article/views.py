from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.


class PostList(ListView):
    queryset = Post.objects.publish()
    template_name = "index.html"


class PostDetail(DetailView):
    model = Post
    template_name = "post_detail.html"
