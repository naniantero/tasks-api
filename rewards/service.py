from .models import RewardTemplate


def create_reward(title: str) -> RewardTemplate:
    """
    Create a new reward in the database.
    """
    reward = RewardTemplate.objects.create(title=title)
    return reward
