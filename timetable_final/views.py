from django.shortcuts import render,redirect
from django.views import generic
from django.views.generic import View
from django import views
from rest_framework import serializers
import MySQLdb,json,operator
from collections import OrderedDict
from operator import itemgetter
from peewee import *
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,JsonResponse
import random
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
