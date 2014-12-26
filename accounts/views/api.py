# from django.contrib.auth import get_user_model

from rest_framework import generics, permissions

from ..serializers import ProfileSerializer, ProfileVersionSerializer


class ProfileVersionView(generics.RetrieveUpdateAPIView):
    permission_classes = permissions.IsAuthenticated,
    serializer_class = ProfileVersionSerializer

    def get_object(self):
        return self.request.user


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = permissions.IsAuthenticated,
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user
