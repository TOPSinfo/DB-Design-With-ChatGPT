from django.shortcuts import redirect, HttpResponseRedirect, HttpResponse


def is_logged_in(func):
    """
    This function is used to check if the user is logged in or not.
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(redirect_to="/")
    return wrapper