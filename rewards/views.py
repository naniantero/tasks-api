from urllib.request import Request

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rewards.serializers import RewardSerializer
from rewards.service import create_reward


class CreateRewardView(APIView):
    """
    API endpoint to create a new reward.
    """

    def post(self, request: Request) -> Response:
        serializer = RewardSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        reward_name: str = serializer.validated_data["name"]  # type: ignore
        reward = create_reward(reward_name)
        return Response(RewardSerializer(reward).data, status=status.HTTP_201_CREATED)
