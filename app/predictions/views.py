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
from django.contrib.auth.models import User
import random
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


def get_start_resp(default_start, end, symbol, x):
    start_date_uni = random_date(default_start, end)
    start_date = str(start_date_uni)[0:10]
    url = 'http://1.phisix-api.appspot.com/stocks/'
    start_url = url+symbol+'.'+start_date+'.json'
    start_resp = requests.get(start_url)
    if start_resp.status_code == 404:
        if x > 4:
            res = requests.get("http://phisix-api3.appspot.com/stocks.json", )
            entries = ('AGF', 'APL', 'HOUSE', 'ANI', 'ALHI', 'AP', 'FOOD', 'ABSP', 'AGI',
            'AEV', 'ANS', 'ATN', 'ATNB')
            dum = res.json()
            dum = dum.get('stock')
            dum = entries_to_remove(entries, dum)
            company_list = []
            for company in dum:
                name = company.get('symbol')
                company_list.append(name)
            symbol = random.choice(company_list)
            return get_start_resp(default_start, end, symbol, 0)
        return get_start_resp(default_start, end, symbol, x+1)

    return start_date_uni, start_resp


def check_date(request):
    difference = request.data.get('range', '')
    end = datetime.today() - timedelta(days=difference)
    default_start = datetime.strptime('01012010', "%d%m%Y")

    symbol = request.data.get('symbol')
    url = 'http://1.phisix-api.appspot.com/stocks/'

    start_date, start_resp = get_start_resp(default_start, end, symbol, 0)
    print start_resp.status_code
    end_date = start_date + timedelta(days=difference)

    end_date = str(end_date)[0:10]
    end_url = url+symbol+'.'+end_date+'.json'
    end_resp =  requests.get(end_url)
    if end_resp.status_code == 404:
        return check_date(request)
    print end_resp.status_code
    end_data = end_resp.json()

    start_data = start_resp.json()
    start_price = start_data.get('stock')[0].get('price').get('amount')

    end_price = end_data.get('stock')[0].get('price').get('amount')

    return str(start_date)[0:10], end_date


class Index(APIView):
    def get(self, request,):
        return Response({"accounts ": "v1", })


class GenerateDate(APIView):
    def get(self, request):
        return Response({"data ": "range(int)", })

    def post(self, request,):
        start_date, end_date = check_date(request)
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

        user = User()
        profile = UserProfile.objects.all()[0]
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
        to_add = float(bet) * percentage
        increase = float(bet) + to_add

        #if not start_date and not end_date and not symbol:
        #    return Response({"status": "fail", "message": "incomplete inputs"})
        user = User.objects.all()[0]
        prediction = Prediction()
        prediction.user = user
        prediction.symbol = symbol
        prediction.choice = choice
        prediction.start_date = start_date
        prediction.end_date = end_date
        prediction.bet = bet
        prediction.balance = balance + to_add
        profile.balance = balance + to_add
        profile.save()
        if choice == "Up" and to_add > 0:
            prediction.result = True
        elif choice == "Down" and to_add < 0:
            prediction.result = True
        else:
            prediction.result = False
        prediction.save()

        return Response({"status": "success", 'start_price': start_price, 'end_price': end_price, 'result':prediction.result})


class StartEnd(APIView):
    def post(self, request):
        symbol = request.data.get('symbol', '')
        start_date = request.data.get('start_date', '')
        end_date = request.data.get('end_date', '')
        url = 'http://1.phisix-api.appspot.com/stocks/'
        start_url = url+symbol+'.'+start_date+'.json'
        start_resp = requests.get(start_url)
        print start_date, "START DATEEE"
        start_data = start_resp.json()
        start_price = start_data.get('stock')[0].get('price').get('amount')

        end_url = url+symbol+'.'+end_date+'.json'
        end_resp = requests.get(end_url)
        print end_date, "END DATEEE"
        end_data = end_resp.json()
        end_price = end_data.get('stock')[0].get('price').get('amount')

        return Response({"status": "success", 'start_price': start_price, 'end_price': end_price})


def entries_to_remove(entries, the_dict):
    for key in entries:
        if key in the_dict:
            del the_dict[key]
    return the_dict


class CompanyList(APIView):
    """docstring for ."""
    def get(self, request):
        res = requests.get("http://phisix-api3.appspot.com/stocks.json", )
        entries = ('AGF', 'APL', 'HOUSE', 'ANI', 'ALHI', 'AP', 'FOOD', 'ABSP', 'AGI',
        'AEV', 'ANS', 'ATN', 'ATNB')
        dum = res.json()
        dum = dum.get('stock')
        dum = entries_to_remove(entries, dum)
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
