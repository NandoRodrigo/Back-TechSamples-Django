from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):

        return bool(request.user.is_authenticated and
                    request.user.is_admin == True)


class IsAnalyst(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True

        return bool(request.user.is_authenticated and not
                    request.user.is_admin == True)


class IsUserCreationOrList(BasePermission):
    def has_permission(self, request, view):

        if request.method == 'POST' and request.user.is_authenticated:
            return True

        return bool(request.user.is_authenticated and
                    request.user.is_admin == True)


class IsUserUpdatePassword(BasePermission):
    def has_permission(self, request, view):

        if str(request.user.uuid) in request.META['PATH_INFO'] and request.user.is_authenticated:
            return True


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True

        return bool(request.user.is_authenticated and
                    request.user.is_admin == True)
