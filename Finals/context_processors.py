from django.utils import timezone


def current_login_time(request):
    # Get the current login time
    login_time = timezone.now()
    return {'current_login_time': login_time}