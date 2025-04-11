from .models import TaskTemplate


def create_task(name: str) -> TaskTemplate:
    """
    Create a new task in the database.
    """
    task = TaskTemplate.objects.create(name=name)
    return task
