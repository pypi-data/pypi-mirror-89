import inspect

from django.core.exceptions import ImproperlyConfigured

from .collections import list_duplicates


def permission_for(model):
    """Decorate function to overwriting permission of specific mutation."""

    def decorate(fn):
        if not hasattr(fn, "_permissions"):
            fn._permissions = []
        fn._permissions.append(model)
        return fn

    return decorate


def object_permission_for(model):
    """Decorate function to overwriting object permission of specific model."""

    def decorate(fn):
        if not hasattr(fn, "_object_permissions"):
            fn._object_permissions = []
        fn._object_permissions.append(model)
        return fn

    return decorate


class BasePermission(object):
    """Basic permission class to be extended by any permission implementation.

    In combination with the decorators `@permission_for` and `@object_permission_for` a custom
    permission class can define permission on basis of models.

    Per default it returns True but default can be overwritten to define a permission for
    `BaseModel`

    A custom permission class could look like this:
    ```
    >>> from generic_permissions.permissions import BasePermission
    ... from tests.models import BaseModel, Model1
    ...
    ... class CustomPermission(BasePermission):
    ...     @permission_for(BaseModel)
    ...     def has_permission_default(self, request):
    ...         # change default permission to False when no more specific
    ...         # permission is defined.
    ...         return False
    ...
    ...     @permission_for(Model1)
    ...     def has_permission_for_document(self, request):
    ...         return True
    ...
    ...     @object_permission_for(Model1)
    ...     def has_object_permission_for_document(self, request, instance):
    ...         return request.user.username == 'admin'
    ```
    """

    def __init__(self):
        perm_fns = inspect.getmembers(self, lambda m: hasattr(m, "_permissions"))
        perm_muts = [
            permission.__name__ for _, fn in perm_fns for permission in fn._permissions
        ]
        perm_muts_dups = list_duplicates(perm_muts)
        if perm_muts_dups:
            raise ImproperlyConfigured(
                f"`permission_for` defined multiple times for "
                f"{', '.join(perm_muts_dups)} in {str(self)}"
            )
        self._permissions = {
            permission: fn for _, fn in perm_fns for permission in fn._permissions
        }

        obj_perm_fns = inspect.getmembers(
            self, lambda m: hasattr(m, "_object_permissions")
        )
        obj_perm_muts = [
            permission.__name__
            for _, fn in obj_perm_fns
            for permission in fn._object_permissions
        ]
        obj_perm_muts_dups = list_duplicates(obj_perm_muts)
        if obj_perm_muts_dups:
            raise ImproperlyConfigured(
                f"`object_permission_for` defined multiple times for "
                f"{', '.join(obj_perm_muts_dups)} in {str(self)}"
            )
        self._object_permissions = {
            permission: fn
            for _, fn in obj_perm_fns
            for permission in fn._object_permissions
        }

    def has_permission(self, model, request):
        for cls in model.mro():
            if cls in self._permissions:
                return self._permissions[cls](request)

        return True

    def has_object_permission(self, model, request, instance):
        for cls in model.mro():
            if cls in self._object_permissions:
                return self._object_permissions[cls](request, instance)

        return True


class AllowAny(BasePermission):
    pass
