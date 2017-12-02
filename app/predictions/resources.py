from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Prediction


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ['symbol', 'choice', 'start_date', 'end_date', 'result']
