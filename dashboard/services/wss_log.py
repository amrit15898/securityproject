from django.shortcuts import redirect
from django.contrib.auth.hashers import check_password
from dashboard.models import wss_auth_user


def wss_login_required(redirect_to):
    def wrapper(view_func):
        def wrapped(request, *args, **kwargs):
            try:
                if request.session["wss-auth-username"] and request.session["wss-auth-password"]:
                    usr = wss_auth_user.objects.get(username=request.session["wss-auth-username"])
                    if check_password(request.session["wss-auth-password"], usr.password):
                        request.wss_user = usr
                        return view_func(request, *args, **kwargs)
                    else:
                        return redirect(redirect_to)
            except:
                return redirect(redirect_to)



        return wrapped
    return wrapper

