from django.db.models import Manager
from . import querysets as article_queryset


class PostManager(Manager):
    def get_queryset(self) -> article_queryset.PostQuerySet:
        return article_queryset.PostQuerySet(self.model, using=self._db)

    def active(self) -> article_queryset.PostQuerySet:
        return self.get_queryset().active()
