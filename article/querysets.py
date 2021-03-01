from django.db.models import QuerySet


class PostQuerySet(QuerySet):
    def draft(self) -> "PostQuerySet":
        return self.filter(status="draft")

    def publish(self) -> "PostQuerySet":
        return self.filter(status="publish")
