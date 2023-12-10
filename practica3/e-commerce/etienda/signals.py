import logging

from django.contrib.auth.signals import user_logged_in, user_login_failed, user_logged_out
from django.dispatch import receiver
from django.http import HttpResponse


logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def post_login(sender, request, user, **kwargs):
    logger.info(f'User: {user.username} logged in')
    logger.warning(f'User: {user.username} logged in')

    auth_cookie = "autenticado"
    response = HttpResponse()
    response.set_cookie('auth', auth_cookie) 


@receiver(user_logged_out)
def post_logout(sender, request, user, **kwargs):
    logger.info(f'User: {user.username} logged out')
    logger.warning(f'User: {user.username} logged out')
    
    response = HttpResponse()
    response.delete_cookie('auth')  # Delete the 'auth' cookie
    


@receiver(user_login_failed)
def post_login_fail(sender, credentials, request):
    logger.info(f'Login failed with credentials: {credentials}')