from django.contrib.auth.middleware import get_user
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class UpdateLastActivityMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        user = get_user(request)
        if user.is_authenticated:
            user.userprofile.last_activity = timezone.now()
            user.userprofile.save()
        return None
