from django.shortcuts import redirect

def student_required(view_func):
    print("Entered the Post Space of the Placement student_required")
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('whom') != "STUDENT":
            return redirect('student_login')  # Redirect to login if not a student
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def staff_required(view_func):
    print("Entered the Post Space of the Placement staff_required")
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('whom') != "STAFF":
            return redirect('staff_login')  # Redirect to login if not staff
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def specific_role_required(allowed_roles):
    print("Entered the Post Space of the Placement specific_role_required")
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user_role = request.session.get('role')
            if request.session.get('whom') != "STAFF"  or user_role not in allowed_roles:
                return redirect('staff_login')  # Redirect to login if not authorized
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator



def admin_specific_role_required(allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user_role = request.session.get('role')
            if request.session.get('whom') != "ADMIN" or user_role not in allowed_roles:
                return redirect('staff_login')  # Redirect to login if not authorized
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('whom') != "ADMIN":
            return redirect('staff_login')  # Redirect to login if not staff
        return view_func(request, *args, **kwargs)
    return _wrapped_view