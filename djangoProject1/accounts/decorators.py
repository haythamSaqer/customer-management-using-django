from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_fanc):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_fanc(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_fanc):
        def wrapper_fanc(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_fanc(request, *args, **kwargs)
            else:
                return HttpResponse("you are not authorized to view this page")
        return wrapper_fanc
    return decorator


def admin_only(view_fanc):
    def wrapper_fanc(request, *args, **kwargs):

        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'admin':
            return view_fanc(request, *args, **kwargs)
        elif group == 'customer':
            return redirect('user-page')
    return wrapper_fanc
