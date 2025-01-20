from rest_framework import permissions

class CheckAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.role == 'admin'


class CheckAll(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'


class CheckAppointment(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method  in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'patient'



class CheckMedicalRecord(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'doctor'