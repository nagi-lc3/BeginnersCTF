from BeginnersCTF.ctf.forms import UsernameChangeForm
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib import messages
