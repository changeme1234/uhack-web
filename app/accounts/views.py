# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import UserProfile
from django.db import IntegrityError
from django.contrib.auth.models import User


class Index(APIView):
    def get(self, request,):
        return Response({"accounts ": "v1", })


class Signup(APIView):
    def get(self, request,):
        return Response({"Signup ": "v1", })

    def post(self, request):
        username = request.data.get('username', '')
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        user = User()
        user.username = username
        user.email = email
        user.set_password(password)
        try:
            user.save()
        except IntegrityError:
            return Response({"status": "fail", "message": "username already existed"})

        userprofile = UserProfile()
        userprofile.user = user
        userprofile.save()
        return Response({"status": "success"})


class Login(APIView):
    def get(self, request,):
        return Response({"Login": "v1"})

    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(username=username, password=password)
        print user, "DSADASDSA"
        if user is not None:
            print "success"
            return Response({"status": "success"})
        else:
            return Response({"status": "fail", "message":"incorrect credentials"})
