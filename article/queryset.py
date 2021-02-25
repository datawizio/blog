from django.db.models import QuerySet


class PostQuerySet(QuerySet):

    def active(self) -> "PostQuerySet":
        return self.filter(active=True)
