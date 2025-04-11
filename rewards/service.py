from .models import RewardTemplate


def create_reward(name: str) -> RewardTemplate:
    """
    Create a new reward in the database.
    """
    reward = RewardTemplate.objects.create(name=name)
    return reward
