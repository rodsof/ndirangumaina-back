from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from . import serializers
from . import permissions
from rest_framework import generics
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from . import models
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class UserProfileViewSet(viewsets.ModelViewSet):
    """handle creating and updating profiles"""
    serializer_class = serializers.ProfileSerializer
    queryset = models.UserProfile.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile, )

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email', 'organization')


class UserLoginView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileData(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    serializer_class = serializers.DataSerializer
    parser_classes = (MultiPartParser, FileUploadParser, )

    permission_classes = (
        permissions.EditUserData,
        IsAuthenticated,
    )

    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', )

    queryset = models.UserProfileData.objects.all()
    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)


class ListFeaturedData(generics.ListAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (
        IsAuthenticated, 
    )

    queryset = models.FeaturedData.objects.all()
    serializer_class = serializers.FeaturedSerializer




