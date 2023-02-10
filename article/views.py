from django.db.models import Count
from django.views.generic import ListView, DetailView, TemplateView
from .models import Post

# Create your views here.


class Index(TemplateView):
    template_name="index.html"

class PostList(ListView):
    queryset = Post.objects.publish().annotate(like_count=Count("likes"))
    template_name = "blog.html"


class PostDetail(DetailView):
    model = Post
    template_name = "article.html"

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["last_articles"] = (
            self.get_queryset().exclude(pk=self.object.pk).order_by("-created")[:3]
        )
        return context
