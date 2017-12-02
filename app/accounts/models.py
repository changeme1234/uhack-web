# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User


from django.db import models

RANK_CHOICES = (
    ("Herald", "Herald"),
    ("Guardian", "Guardian"),
    ("Crusader", "Crusader"),
    ("Archon", "Archon"),
    ("Legend", "Legend"),
    ("Ancient", "Ancient"),
    ("Divine", "Divine"),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(blank=True, null=True, default=1000.0)
    rank = models.CharField(
        max_length=10,
        choices=RANK_CHOICES,
        default='Herald',
    )
