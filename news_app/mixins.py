from django.core.exceptions import PermissionDenied

class UserIsOwnerMixin:
    owner_field = "author"
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if getattr(obj, self.owner_field, None) != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
