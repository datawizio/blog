from rest_framework.viewsets import GenericViewSet


class GenericViewSetMixin(GenericViewSet):
    # Get serializer class for different action (create, list, retrieve, etc.)
    serializer_classes = {}

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)
