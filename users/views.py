# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalMemberAccess=false
import uuid

from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Group, GroupMembership, User
from users.serializers import GroupSerializer, JoinGroupSerializer
from users.service import join_group


class CreateGroupView(APIView):
    def post(self, request: Request) -> Response:
        group_name = request.data.get('group_name')
        admin_name = request.data.get('admin_name')

        if not group_name or not admin_name:
            return Response({'error': 'group_name and admin_name are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the group
        group = Group.objects.create(name=group_name)

        # Create the admin user (with a generated username/email for now)
        user = User.objects.create(
            username=f"admin_{uuid.uuid4().hex[:8]}",
            email=f"{uuid.uuid4().hex[:8]}@example.com",
            first_name=admin_name
        )

        # Attach user to group as admin
        GroupMembership.objects.create(
            user=user,
            group=group,
            role='admin'
        )

        return Response({
            'group_id': str(group.id),
            'admin_user_id': user.id,
            'admin_username': user.username
        }, status=status.HTTP_201_CREATED)


class GroupDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer()


class JoinGroupView(APIView):
    def post(self, request: Request, group_id: int):
        serializer = JoinGroupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        name = serializer.validated_data.get('name', '')
        device_id = serializer.validated_data.get(
            'device_id', '')  # this is required, but anyway

        user = join_group(group_id, device_id, name)

        if not user:
            return Response({'error': 'Group not found or something else went wrong'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'user_id': user.id,
            'username': user.username,
            'group_id': str(group_id)
        }, status=status.HTTP_201_CREATED)
