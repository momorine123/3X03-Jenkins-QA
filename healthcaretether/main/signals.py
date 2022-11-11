from django.contrib.auth.signals import user_logged_in,user_logged_out,user_login_failed
from django.dispatch import receiver

import logging
logger = logging.getLogger('main')

@receiver(user_logged_in)
def log_user_login(sender,request,user,**kwargs):
    message = "user {} logged in through page {}".format(user.username,request.META.get('HTTP_REFERER'))
    logger.info(message)

# @receiver(user_login_failed)
# def log_user_login_fail(sender,credentials,request,**kwargs):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     message = "user {} failed log in through page {}".format(ip,request.META.get('HTTP_REFERER'))
#     logger.error(message)

@receiver(user_logged_out)
def log_user_logout(sender,request,user,**kwargs):
    message = "user {} logged out through page {}".format(user.username,request.META.get('HTTP_REFERER'))
    logger.info(message)