# myapp/decorators.py
from django.shortcuts import render
from functools import wraps

def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and (request.user.is_superuser or request.user.role in roles):
                return view_func(request, *args, **kwargs)
            return render(request, 'permission_denied.html')
        return _wrapped_view
    return decorator
