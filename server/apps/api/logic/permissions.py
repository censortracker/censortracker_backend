from rest_framework.permissions import BasePermission


class AllowByHeaders(BasePermission):

    def has_permission(self, request, view):
        censortracker_d = request.META.get('HTTP_CENSORTRACKER_D')
        censortracker_v = request.META.get('HTTP_CENSORTRACKER_V')

        if censortracker_d and censortracker_v:
            return True

        return False
