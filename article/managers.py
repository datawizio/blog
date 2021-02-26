from django.db.models import Manager
from .querysets import PostQuerySet


class PostManager(Manager):
    def get_queryset(self) -> PostQuerySet:
        return PostQuerySet(self.model, using=self._db)

    def draft(self) -> PostQuerySet:
        return self.get_queryset().draft()

    def publish(self) -> PostQuerySet:
        return self.get_queryset().publish()