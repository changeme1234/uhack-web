# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from core.models import Base

CHOICES = (
    ("Up", "Up"),
    ("Down", "Down"),
)


class Prediction(Base):
    user = models.ForeignKey(User,)
    symbol = models.CharField(blank=False, default="", max_length=10)
    choice = models.CharField(
        max_length=4,
        choices=CHOICES,
        default='Up',
    )
    start_date = models.DateField()
    end_date = models.DateField()
    bet = models.IntegerField(blank=False)
    balance = models.FloatField(blank=False)
    result = models.BooleanField(default=False)
