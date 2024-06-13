"""
File for defining modles in Django notation
"""

import datetime
from enum import Enum, auto

from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

GROUP_TOKEN_LENGTH = 32

class Group(models.Model):
    """
    Class to represent a Group model
    """

    tag = models.CharField(null=False, max_length=50)
    is_public = models.BooleanField(null=False, default=True)

    name = models.CharField(null=True, max_length=50)
    token = models.CharField(null=False, max_length=GROUP_TOKEN_LENGTH)

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="users_groups")

    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE, related_name="led_group"
    )

    supergroup = models.ForeignKey(
        "self", null=True, on_delete=models.CASCADE, related_name="groups"
    )

    def __str__(self) -> str:
        return self.tag


class Goal(models.Model):
    """
    Class to represent a Goal model
    """

    name = models.CharField(null=False, max_length=50)
    is_active = models.BooleanField(null=False, default=True)

    deadline = models.DateTimeField(null=True)
    alert_period = models.DurationField(null=True)

    group = models.ForeignKey(
        "Group", null=False, on_delete=models.CASCADE, related_name="goals"
    )

    supergoal = models.ForeignKey(
        "self", null=True, on_delete=models.CASCADE, related_name="goals"
    )

    @property
    def final_value(self) -> int:
        result = 0

        duties = Duty.objects.filter(goal=self).all()
        for duty in duties:
            result += duty.final_value

        return result

    @property
    def current_value(self) -> int:
        result = 0

        duties = Duty.objects.filter(goal=self).all()
        for duty in duties:
            result += duty.current_value

        return result

    def __str__(self) -> str:
        return self.name


class Duty(models.Model):
    """
    Class to represent a Duty model
    """

    final_value = models.IntegerField(null=False, default=0)
    current_value = models.IntegerField(null=False, default=0)

    deadline = models.DateTimeField(null=True)
    alert_period = models.DurationField(null=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE, related_name="duties"
    )
    goal = models.ForeignKey(
        "Goal", null=False, on_delete=models.CASCADE, related_name="duties"
    )


class EventType(Enum):
    GroupCreated = auto()
    GroupOverdued = auto()
    GoalCreate = auto()
    GoalReached = auto()
    GoalClosed = auto()
    UserPaid = auto()
    UserOverdued = auto()
    ReportPosted = auto()

    def __int__(self):
        return self.value

EVENT_MESSAGES = {
    EventType.GroupCreated: "group has been created",
    EventType.GroupOverdued: "group has overdued his pay",
    EventType.GoalCreate: "goal has been created",
    EventType.GoalReached: "goal has been reached",
    EventType.GoalClosed: "goal has been closed",
    EventType.UserPaid: "user has paid his share",
    EventType.UserOverdued: "user has overdued his pay",
    EventType.ReportPosted: "report has been posted"
}

class Event(models.Model):
    """
    Class to represent a Event model
    """

    type = models.IntegerField(null=False, default=0)
    text = models.CharField(null=False, max_length=500, default="")
    timestamp = models.DateTimeField(null=False, default=datetime.datetime.now)

    group = models.ForeignKey(
        "Group", null=True, on_delete=models.CASCADE, related_name="events"
    )
    goal = models.ForeignKey(
        "Goal", null=True, on_delete=models.CASCADE, related_name="events"
    )


class Report(models.Model):
    """
    Class to represent a Report model
    """

    text = models.CharField(null=True, max_length=1024)

    goal = models.ForeignKey(
        "Goal", null=False, on_delete=models.CASCADE, related_name="reports_goal"
    )


class Image(models.Model):
    """
    Class to represent a Image model
    """

    image = models.ImageField(
        null=False,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=("png", "jpg", "jpeg"))],
    )

    group = models.ForeignKey(
        "Group", null=True, on_delete=models.CASCADE, related_name="group"
    )

    report = models.ForeignKey(
        "Report", null=True, on_delete=models.CASCADE, related_name="report"
    )
