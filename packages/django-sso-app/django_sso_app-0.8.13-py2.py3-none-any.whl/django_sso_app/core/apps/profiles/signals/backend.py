import logging

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in

from ..utils import get_or_create_user_profile, is_django_staff

logger = logging.getLogger('django_sso_app.core.apps.profiles.signals')

User = get_user_model()


# user

@receiver(post_save, sender=User)
def create_update_user_profile(sender, instance, created, **kwargs):
    """
    Creates new user profile if not already done.
    """
    user = instance

    if kwargs['raw']:
        # https://github.com/django/django/commit/18a2fb19074ce6789639b62710c279a711dabf97
        # setting property flag
        setattr(user, '__dssoa__loaddata', True)
        return

    if created:
        logger.debug('backend signals user created')

        setattr(instance, '__dssoa__creating', True)

        profile = get_or_create_user_profile(user, commit=True)

        logger.debug('new profile created "{}"'.format(profile))

        # refreshing user instance property
        user.sso_app_profile = profile

    else:
        logger.debug('backend signals user updated')
        profile = get_or_create_user_profile(user, commit=False)

        # rev should update only for non django staff users
        update_rev = not is_django_staff(user)

        # replaced by '__user_loggin_in'
        # if user.previous_serialized_as_string == user.serialized_as_string:
        if getattr(user, '__dssoa__creating', False):
            logger.info('user _creating')
            update_rev = False
        elif getattr(user, '__dssoa__user_loggin_in', False):
            logger.info('user loggin in')
            update_rev = False
        elif user.password_has_been_hardened:
            logger.info('password_has_been_hardened')
            update_rev = False
        elif is_django_staff(user):
            logger.info('User is staff, skipping rev update')
            update_rev = False

        # align profile user fields
        if user.email_has_been_updated:
            # aligning sso_app_profile django_user_email
            profile.django_user_email = user.sso_app_new_email

        if user.username_has_been_updated:
            # aligning sso_app_profile django_user_username
            profile.django_user_username = user.sso_app_new_username

        if update_rev:
            logger.info('Update rev by User signal while user fields have been updated')
            profile.update_rev(True)  # updating rev


@receiver(user_logged_in)
def create_profile_for_legacy_users(**kwargs):
    """
    Post login profile creation for user models created before django_sso_app.
    """
    user = kwargs['user']

    _profile = get_or_create_user_profile(user)
    # setattr(user, 'sso_app_profile', _profile)

    logger.debug('Profile, "{}" LOGGED IN!!!'.format(_profile))
