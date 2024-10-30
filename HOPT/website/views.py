from django.shortcuts import render, redirect
from django.db import connection
from .forms import LoginForm, CustomUserCreationForm
from .models import CustomUser
from django.http import Http404
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
import random
import string

# Trang chủ
def Home(request):
    return render(request, 'Home.html')

