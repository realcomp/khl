# from django.contrib.auth import get_user_model

from rest_framework import generics, permissions

from ..serializers import UserVersionSerializer


class UserVersionView(generics.RetrieveUpdateAPIView):
    permission_classes = permissions.IsAuthenticated,
    serializer_class = UserVersionSerializer

    def get_object(self):
        return self.request.user
