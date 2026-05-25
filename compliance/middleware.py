import ipaddress
from django.utils import timezone
from django.contrib.auth import get_user_model


class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip

    @staticmethod
    def log_action(request, action, model_name='', object_id='', object_repr='', description='', is_sensitive=False):
        from .models import AuditLog
        user = request.user
        AuditLog.objects.create(
            user=user if user.is_authenticated else None,
            username=user.get_username() if user.is_authenticated else 'anonymous',
            action=action,
            model_name=model_name,
            object_id=str(object_id) if object_id else '',
            object_repr=str(object_repr)[:255] if object_repr else '',
            description=str(description)[:1000] if description else '',
            ip_address=AuditMiddleware.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            request_method=request.method,
            request_path=request.path[:500],
            is_sensitive=is_sensitive,
        )
