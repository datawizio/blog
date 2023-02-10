from django import template


register = template.Library()


@register.inclusion_tag("components/likeBtn.html", takes_context=True)
def like_btn(context):
    return {"post": context["post"]}
