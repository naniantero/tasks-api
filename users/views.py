# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalMemberAccess=false
import uuid
from urllib.request import Request

from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import Group
from users.serializers import (CustomTokenObtainPairSerializer,
                               GroupSerializer, JoinGroupSerializer, JoinGroupWithInviteSerializer,
                               RegisterAdminSerializer)
from users.service import admin_join_group, join_group_with_invite, register_admin_and_create_group

User = get_user_model()


@method_decorator(csrf_exempt, name='dispatch')
class RegisterAdminView(APIView):
    permission_classes = []

    def post(self, request: Request) -> Response:
        serializer = RegisterAdminSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data.get("username")
        res = register_admin_and_create_group(username)
        return Response(res, status=status.HTTP_201_CREATED)


class GroupDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class AdminJoinGroupView(APIView):
    def post(self, request: Request, group_id: uuid.UUID) -> Response:
        serializer = JoinGroupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        name = serializer.validated_data.get('name', '')
        device_id = serializer.validated_data.get(
            'device_id', '')  # this is required, but anyway

        user = admin_join_group(group_id, device_id, name)

        if not user:
            return Response({'error': 'Group not found or something else went wrong'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'user_id': user.id,
            'username': user.username,
            'group_id': str(group_id)
        }, status=status.HTTP_201_CREATED)


class JoinGroupWithInviteView(APIView):
    def post(self, request: Request) -> Response:
        serializer = JoinGroupWithInviteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token = serializer.validated_data.get("token")
        user = join_group_with_invite(token)

        if (not user):
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'user_id': user.id,
            'username': user.username,
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer  # type: ignore
