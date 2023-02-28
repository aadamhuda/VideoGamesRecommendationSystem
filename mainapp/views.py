from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, authenticate, login
from .forms import LoginForm, SignUpForm
from .models import Question, Game, Profile
from django.contrib import messages
from django.contrib.auth import logout
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
import json, datetime
import re

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
#---------------------------------------quiz------------------------------------------------
def get_questions(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        return JsonResponse (
            [i.to_dict() for i in Question.objects.all()]
         , safe=False)

@csrf_exempt
def store_temp_profile(request: HttpRequest) -> JsonResponse:
    success = False
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if (len(data['picked_items']) > 0):
            temp_profile = []
            for picked in data['picked_items']:
                print(picked)
                if (picked != None):
                    success = True
                    sub_list = picked.split("; ")
                    for item in sub_list:
                        if (item != 'None'):
                            temp_profile.append(item)
                else:
                    success = False
                    return JsonResponse({
                        'success': success
                    })
        if (success == True):
            num_preference = temp_profile.pop(0)
            if(Profile.objects.filter(user_id=data['user_id']).exists()):
                print("exists")
                player_profile = Profile.objects.get(user_id=data['user_id'])
                player_profile.genre = temp_profile
                player_profile.num_players_preference = num_preference
                player_profile.save()
            else:
                 player_profile = Profile.objects.create(
                    keyword = "",
                    genre = temp_profile,
                    num_players_preference = num_preference,
                    user_id = data['user_id'],
                 )
        return JsonResponse({
            'success': success
        })
    
@csrf_exempt
def store_profile(request: HttpRequest) -> JsonResponse:
    success = False
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if (len(data['games_choice']) >0):
            genres = []
            keywords = []
            words = word_count()
            for game in data['games_choice']:
                query = Game.objects.all().filter(title = game).values()
                df = pd.DataFrame.from_records(query)
                genres.extend((df['genre'].iloc[0]).split(", "))
                keywords.extend(return_keywords(re.findall(r'\w+', df['summary'].iloc[0]), words))

            keywords.sort(key = lambda x: x[1])
            cleaned_keywords = []
            [cleaned_keywords.append(kw) for kw in keywords if kw not in cleaned_keywords ]
            profile_keywords = []
            [profile_keywords.append(kw[0]) for kw in cleaned_keywords if kw[1]>1 and kw[1]<501]
            if(Profile.objects.filter(user_id=data['user_id']).exists()):
                player_profile = Profile.objects.get(user_id=data['user_id'])
                player_profile.keyword = profile_keywords
                player_profile.genre = genres
                player_profile.save()
            else:
                pass

            return JsonResponse({
                'success': success
            })
        
def word_count():
    games = pd.DataFrame.from_records(Game.objects.all().values())
    vec = CountVectorizer().fit(games['summary'])
    bag_of_words = vec.transform(games['summary'])
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [[word, sum_words[0, idx]] for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq

def return_keywords(summary, words):
    keyword_quantities = []
    for word in summary:
        for keyword in words:
            if word == keyword[0]:
                keyword_quantities.append(keyword)
    return keyword_quantities

        
def get_quiz_games(request: HttpRequest) -> JsonResponse:
    success = False
    if request.method == 'GET':
        data = json.loads(request.session.__getitem__("_auth_user_id"))
        if (Profile.objects.filter(user_id=data).exists()):
            profile = Profile.objects.get(user_id=data)
            games = filter_num_players(profile.get_num_players_preference())
            #games = pd.DataFrame.from_records(Game.objects.all().values('title','genre'))
            user_profile = pd.DataFrame({
                'title': ["user_profile_temp"],
                'genre': [profile.get_genre()]
            })
            games = pd.concat([games, user_profile],ignore_index=True)
            print(games.iloc[[len(games.index)-1]])
            rec_games = generate_recomendations(games, 'genre')
            success =  True
            print (rec_games)
            print (len(rec_games))

        return JsonResponse ({
                'games_list' : rec_games,
                'success' : success,
            })
    
def user_recommendations(request: HttpRequest) -> JsonResponse:
    success = False
    if request.method == 'GET':
        data = json.loads(request.session.__getitem__("_auth_user_id"))
        if (Profile.objects.filter(user_id=data).exists()):
            profile = Profile.objects.get(user_id=data)
            games = filter_num_players(profile.get_num_players_preference())
            user_profile = pd.DataFrame({
                'title': ["user_profile_temp"],
                'genre': [profile.get_genre()],
                'summary': [profile.get_keyword()],
            })
            games = pd.concat([games, user_profile],ignore_index=True)
            print(games.iloc[[len(games.index)-1]])
            rec_games_genre = generate_recomendations(games, 'genre')
            rec_games_keywords = generate_recomendations(games, 'summary')
            success =  True
            recs = []
            recs.extend(rec_games_genre[:10])
            recs.extend(rec_games_keywords[:20])
            rec_games = []
            [rec_games.append(game) for game in recs if game not in rec_games]
            rec_games = rec_games[:20]
        return JsonResponse ({
                'games_list' : rec_games,
                'success' : success,
            })


def filter_num_players(num_players_preference):
    if(num_players_preference == 'Singleplayer'):
        query = Game.objects.exclude(num_players__contains = 'Online Multiplayer Up to').values()
        q1 = query.filter(num_players = '1 Player').values()
        q2 = query.filter(num_players__contains = 'No Online Multiplayer').values()
        q3 = query.filter(num_players__contains = 'Up to').values()
        query = q1 | q2 | q3
    elif(num_players_preference == 'Coop'):
        query = Game.objects.all().values()
        q1 = query.filter(num_players = '1 Player').values()
        q2 = query.filter(num_players__contains = 'No Online Multiplayer').values()
        q3 = query.filter(num_players__contains = 'Up to').values()
        q4 = query.filter(num_players__contains = '1-').values() 
        query = q1 | q2 | q3 | q4
    elif(num_players_preference == 'Multiplayer'):
        query = Game.objects.exclude(num_players__contains = '1 Player').exclude(num_players__contains = 'No Online Multiplayer').values()
    else:
        query = Game.objects.all().values()

    return pd.DataFrame.from_records(query)


def generate_recomendations(games, field):
        tfidf = TfidfVectorizer(stop_words='english')
        games[field] = games[field].fillna('')
        overview_matrix = tfidf.fit_transform(games[field])
        print(overview_matrix.shape)
        similarity_matrix = linear_kernel(overview_matrix,overview_matrix)
        mapping = pd.Series(games.index, index = games['title'])
        user_index = mapping["user_profile_temp"]
        similarity_score = list(enumerate(similarity_matrix[user_index]))
        similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
        similarity_score = similarity_score[1:200]
        games_index = [i[0] for i in similarity_score]
        print(games['title'].iloc[games_index])
        rec_games = []
        [rec_games.append(game) for game in games['title'].iloc[games_index] if game not in rec_games ]
        return rec_games

def load_db(request: HttpRequest) -> HttpResponse:
    games = pd.read_csv('.\mainapp\static\metacritic_games_master.csv')
    Game.objects.all().delete()
    rows = games.iterrows()
    objs = [
        Game(
            id = index,
            title = row['title'],
            release_date = row['release_date'],
            genre = row['genre'],
            platforms = row['platforms'],
            developer = row['developer'],
            esrb_rating = row['esrb_rating'],
            esrbs = row['ESRBs'],
            metascore = row['metascore'],
            userscore = row['userscore'],
            num_players = row['num_players'],
            summary = row['summary'],
        )
        for index, row in rows
    ]
    Game.objects.bulk_create(objs)
    return JsonResponse({
            'success': True
        })