

class GetDetailSerializerClassMixin:
    """
    Get detail serializer class
    """
    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'create' or self.action == 'update' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()
