import logging

from django.contrib.auth import get_user_model
from django.shortcuts import reverse, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics

from django_filters.rest_framework import DjangoFilterBackend

from allauth.account.adapter import get_adapter

from .forms import UserProfileForm
from .models import Profile
from .serializers import ProfileSerializer, ProfilePublicSerializer, ProfileUnsubscriptionSerializer
from ... import app_settings

from ...permissions import is_staff
from ...utils import invalidate_cookie
from ...mixins import WebpackBuiltTemplateViewMixin

from .filters import ProfileFilter

User = get_user_model()

logger = logging.getLogger('django_sso_app.core.apps.profiles')


class ProfileView(LoginRequiredMixin, WebpackBuiltTemplateViewMixin):
    template_name = "account/profile.html"

    def get_object(self, queryset=None):
        request_user = getattr(self.request, 'user', None)

        return request_user.get_sso_app_profile()

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        self.object = self.get_object()

        if self.object is not None:
            profile = self.object

            user_fields = []
            for field in app_settings.PROFILE_FIELDS:
                user_fields.append((field, getattr(profile, field)))

            context['user_fields'] = user_fields

        return context

    def get(self, request, *args, **kwargs):
        logger.info('Getting profile')

        try:
            return super(ProfileView, self).get(request, *args, **kwargs)

        except:
            logger.exception('Error getting profile')
            raise


class ProfileUpdateView(LoginRequiredMixin, UpdateView, WebpackBuiltTemplateViewMixin):
    model = Profile
    template_name = "account/profile_update.html"
    form_class = UserProfileForm

    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        request_user = getattr(self.request, 'user', None)

        return request_user.get_sso_app_profile()

    def get_context_data(self, *args, **kwargs):
        self.object = self.get_object()

        context = super(WebpackBuiltTemplateViewMixin, self).get_context_data(*args, **kwargs)
        return context

    def get(self, request, *args, **kwargs):
        logger.info('Getting profile update')

        try:
            profile = self.get_object()
            return super(ProfileUpdateView, self).get(request, profile.pk, *args, **kwargs)

        except:
            logger.exception('Error getting profile update')
            raise

    def post(self, request, *args, **kwargs):
        logger.info('Posting profile update')

        try:
            profile = self.get_object()
            response = super(ProfileUpdateView, self).post(request, profile.pk, *args, **kwargs)

        except:
            logger.exception('Error posting profile update')
            raise

        else:
            user = profile.user
            adapter = get_adapter(request)

            adapter.try_update_response_jwt(user, response)

            return response


class ProfileCompleteView(ProfileUpdateView):
    template_name = "account/profile_complete.html"

    def get(self, request, *args, **kwargs):
        logger.info('Getting profile complete')

        if not request.user.sso_app_profile.is_incomplete:
            return redirect(reverse('profile.update'))

        return super(ProfileCompleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logger.info('Posting profile create')

        if not request.user.sso_app_profile.is_incomplete:
            return redirect(reverse('profile.update'))

        return super(ProfileCompleteView, self).post(request, *args, **kwargs)


# api

class ProfileApiViewSet(viewsets.ModelViewSet):
    lookup_field = 'sso_id'
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProfileFilter
    serializer_class = ProfileSerializer

    def get_queryset(self):
        requesting_user = self.request.user

        if is_staff(requesting_user):
            return Profile.objects.all()
        else:
            return Profile.objects.filter(user=requesting_user)

    def list(self, request, *args, **kwargs):
        """
        List profiles
        """
        return super(ProfileApiViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Profile detail
        """
        return super(ProfileApiViewSet, self).retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Profile update
        """
        response = super(ProfileApiViewSet, self).partial_update(request, *args, **kwargs)
        response_status_code = response.status_code
        logger.info('Profile partial_update status code is {}, {}'.format(response_status_code, request.data))

        if response_status_code == 200:
            profile = self.get_object()
            user = profile.user

            adapter = get_adapter(request)
            adapter.try_update_response_jwt(user, response)

        return response


class ProfileCompleteUnsubscriptionApiView(viewsets.GenericViewSet):
    """
    Completely unsubscribe user
    """

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ProfileUnsubscriptionSerializer

    def get_serializer(self, *args, **kwargs):
        request = self.request
        serializer_class = self.get_serializer_class()

        return serializer_class(data=request.data, context={'request': request})

    def completely_unsubscribe(self, request, sso_id, *args, **kwargs):
        logger.info('ProfileCompleteUnsubscriptionApiView {}'.format(sso_id))

        requesting_user = request.user
        serializer = self.get_serializer()

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        adapter = get_adapter(request)

        username = requesting_user.username
        email = requesting_user.email
        password = serializer.data.get('password')

        try:
            adapter.try_completely_unsubscribe(username, email, password)

        except:
            logger.exception('completely_unsubscribe error')
            response = Response('Error unsubscribing completely', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            response = Response('Successfully completely unsubscribed.', status=status.HTTP_200_OK)

        invalidate_cookie(response, app_settings.JWT_COOKIE_NAME)

        return response


class ProfileDetailApiView(generics.RetrieveAPIView):
    """
    Profile detail entrypoint
    """

    lookup_field = 'sso_id'
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.all()

    def get_object(self, *args, **kwargs):
        user = getattr(self.request, 'user', None)

        return user.get_sso_app_profile()
