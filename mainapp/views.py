from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, authenticate, login
from .forms import LoginForm, SignUpForm
from .models import Question
from django.contrib import messages
from django.contrib.auth import logout
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import json, datetime

import pandas as pd
import numpy as np

def index(request: HttpRequest):
    if request.method =='POST':
        form = LoginForm(request.POST, request.FILES)
        user = authenticate(username=form['username'].data, password=form['password'].data)
        if user:
            login(request, user)
            return HttpResponseRedirect("http://localhost:5173/view_items")

        else:
            messages.error(request,'username or password not correct')
            return redirect('./')

    
    else:
        form = LoginForm()
        return render(request, "mainapp/index.html",{
            'form' : form,
    })

def signup(request: HttpRequest) -> HttpResponse:

    Wrong = False

    if (request.method == 'POST'):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your account has been created')
        else:
            Wrong = True
            messages.error(request,'Invalid sign up details')


    form = SignUpForm()
    return render( request, "mainapp/signup.html" , { 
        'form' : form,
        'Wrong' : Wrong,
        } )

def get_user(request: HttpRequest) -> JsonResponse:
    if request.method=='GET':
        return JsonResponse ( {
            'user_id' : request.session.__getitem__("_auth_user_id")
        }, safe=False)

def get_questions(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        return JsonResponse (
            [i.to_dict() for i in Question.objects.all()]
         , safe=False)

def store_temp_profile(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
def loadDataSet(request: HttpRequest) -> HttpResponse:
    games = pd.read_csv('./static/metacritic_games_master.csv')
    tf = TfidfVectorizer(stop_words="english")
    games['genre'] = games['genre'].fillna('')
    
    pass

