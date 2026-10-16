from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
  def has_permission(self, request, view):
    return (
      request.user.is_authenticated and 
      request.user.groups.filter(name="admin").exists()
    )

class IsTeacher(BasePermission):
  def has_permission(self, request, view):
    return (
      request.user.is_authenticated and 
      request.user.groups.filter(name="teacher").exists()
    )

class IsTeacherOrAdmin(BasePermission):
  def has_permission(self, request, view):
    return (
      request.user.is_authenticated and 
      request.user.groups.filter(name__in=["teacher", "admin"]).exists()
    )

class IsTeacherOrAdminForMutationsElsePublic(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
          return True
        
        if not request.user or not request.user.is_authenticated:
          return False
            
        return request.user.groups.filter(name__in=['teacher', 'admin']).exists()