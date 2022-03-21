from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdmin(BasePermission):
  def has_permission(self, request, view):

    return request.user.is_admin


class IsAnalyst(BasePermission):
  def has_permission(self, request, view):
    if request.method in SAFE_METHODS:
      return True

    return not request.user.is_admin
  
class IsUserCreationOrList(BasePermission):
  def has_permission(self, request, view):

    if request.method == 'POST':
      return True

    return bool(request.user.is_authenticated and
                request.user.is_admin == True)
    
class IsUserUpdatePassword(BasePermission):
  def has_permission(self, request, view):
    print(request.user.uuid)
    
    if str(request.user.uuid) in request.META['PATH_INFO']:
      return True
