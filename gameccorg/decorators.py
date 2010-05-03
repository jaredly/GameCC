try:
    from functools import update_wrapper, wraps
except ImportError:
    from django.utils.functional import update_wrapper, wraps  # Python 2.3, 2.4 fallback.

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from django.utils.decorators import available_attrs
from django.utils.http import urlquote
from django.contrib import messages

'''
the following are stolen from django.contrib.auth.decorators, with the
addition of a "message" and "level" attribute, for integration with the
messages framework
'''

def user_passes_test(test_func, message=None, level=messages.ERROR, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """
    if not login_url:
        from django.conf import settings
        login_url = settings.LOGIN_URL

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            path = urlquote(request.get_full_path())
            tup = login_url, redirect_field_name, path
            if message is not None:
                messages.add_message(request, level, message)
            return HttpResponseRedirect('%s?%s=%s' % tup)
        return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)
    return decorator


def my_login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME,
        message=None, level=messages.ERROR):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated(),
        redirect_field_name=redirect_field_name,
        message=message, level=level,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


# vim: et sw=4 sts=4
