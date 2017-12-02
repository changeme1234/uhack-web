# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from rest_framework import status
from django.conf import settings
from .models import Prediction
from random import randrange
from .resources import HistorySerializer
from accounts.models import UserProfile
import json
from django.core.serializers.json import DjangoJSONEncoder
import requests


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


class Index(APIView):
    def get(self, request,):
        return Response({"accounts ": "v1", })


class GenerateDate(APIView):
    def get(self, request):
        return Response({"data ": "range(int)", })

    def post(self, request,):
        difference = request.data.get('range', '')

        end = datetime.today() - timedelta(days=difference)
        default_start = datetime.strptime('01012006', "%d%m%Y")
        start_date = random_date(default_start, end)
        end_date = start_date + timedelta(days=difference)
        start_date = start_date[0:4]
        return Response({"start_date": start_date, "end_date": end_date})


class GetBalance(APIView):
    def get(self, request,):
        user = request.user
        profile = UserProfile.objects.get(user=user.id)
        balance = profile.balance
        return Response({'balance': balance})


class Save(APIView):
    def get(self, request,):
        return Response({'data': 'start_date(date), end_date(date), symbol(str), result(bool)'})
        user = request.user

    def post(self, request):
        user = request.user
        bet = request.data.get('bet', '')
        start_date = request.data.get('start_date', '')
        end_date = request.data.get('end_date', '')
        symbol = request.data.get('symbol', '')
        choice = request.data.get('choice')
        result = request.data.get('result', '')
        bet = request.data.get('bet')

        user = request.user
        profile = UserProfile.objects.get(user=user.id)
        balance = profile.balance

        url = 'http://1.phisix-api.appspot.com/stocks/'
        start_url = url+symbol+'.'+start_date+'.json'
        start_resp = requests.get(start_url)
        start_data = start_resp.json()
        start_price = start_data.get('stock')[0].get('price').get('amount')

        end_url = url+symbol+'.'+end_date+'.json'
        end_resp = requests.get(end_url)
        end_data = end_resp.json()
        end_price = end_data.get('stock')[0].get('price').get('amount')

        difference = end_price - start_price
        percentage = float(difference) / float(end_price)
        to_add = bet * percentage
        increase = bet + to_add

        #if not start_date and not end_date and not symbol:
        #    return Response({"status": "fail", "message": "incomplete inputs"})

        prediction = Prediction()
        prediction.user = user
        prediction.symbol = symbol
        prediction.choice = choice
        prediction.start_date = start_date
        prediction.end_date = end_date
        prediction.result = result
        prediction.bet = bet
        prediction.balance = balance + to_add
        profile.balance = balance + to_add
        profile.save()
        if to_add > 0:
            prediction.result = True
        prediction.save()

        return Response({"status": "success", 'start_price': start_price, 'end_price': end_price})


class CompanyList(APIView):
    """docstring for ."""
    def get(self, request):
        res = requests.get("http://phisix-api3.appspot.com/stocks.json", )
        dum = res.json()
        dum = dum.get('stock')
        company_list = []
        for company in dum:
            name = company.get('symbol')
            company_list.append(name)

        return Response({"symbols":company_list})


class CompanyTrend(APIView):
    def get(self, request):
        pass


class History(APIView):
    def get(self, request,):
        user = request.user
        prediction_list = Prediction.objects.filter(user=user).order_by('-pk')
        serializer = HistorySerializer(prediction_list, many=True)

        return Response(serializer.data)

    def post(self, request):
        return Response({"status": "success"})
