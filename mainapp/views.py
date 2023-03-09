from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, authenticate, login
from .forms import LoginForm, SignUpForm
from .models import MyUser, Question, Game, Profile, PlayList, DislikeList, CompletedList
from django.contrib import messages
from django.contrib.auth import logout
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
import json
import re
import random
from collections import Counter

import pandas as pd
import numpy as np

def index(request: HttpRequest):
    return render(request, "mainapp/index.html")

def log_in(request: HttpRequest):
    if request.method =='POST':
        form = LoginForm(request.POST, request.FILES)
        user = authenticate(username=form['username'].data, password=form['password'].data)
        if user:
            login(request, user)
            return HttpResponseRedirect("http://localhost:5173/Home")

        else:
            messages.error(request,'username or password not correct')
            return redirect('./login')
    else:
        form = LoginForm()
        return render(request, "mainapp/login.html",{
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

def log_out(request):
    logout(request)
    return redirect('./')

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
def get_keywords(game_title):
    words = word_count()
    query = Game.objects.all().filter(title = game_title).values()
    df = pd.DataFrame.from_records(query)
    keywords = return_keywords(re.findall(r'\w+', df['summary'].iloc[0]), words)
    keywords.sort(key = lambda x: x[1])
    cleaned_keywords = []
    [cleaned_keywords.append(kw) for kw in keywords if kw not in cleaned_keywords ]
    profile_keywords = []
    [profile_keywords.append(kw[0]) for kw in cleaned_keywords if kw[1]>1 and kw[1]<301]
    return profile_keywords

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
            rec_games = generate_recomendations(games, 'genre')
            success =  True
            print (rec_games)

        return JsonResponse ({
                'games_list' : rec_games,
                'success' : success,
            })
    
def user_recommendations(request: HttpRequest) -> JsonResponse:
    success = False
    if request.method == 'GET':
        curr_user_id = json.loads(request.session.__getitem__("_auth_user_id"))
        rec_games = []
        if (Profile.objects.filter(user_id=curr_user_id).exists()):
            profile = Profile.objects.get(user_id=curr_user_id)
            print('1')
            games = filter_num_players(profile.get_num_players_preference())
            print('2')
            non_rec_list = generate_non_rec_list(curr_user_id)
            games = filter_list(non_rec_list)
            print('3')
            user_profile = pd.DataFrame({
                'title': ["user_profile_temp"],
                'genre': [profile.get_genre()],
                'summary': [profile.get_keyword()],
            })
            games = pd.concat([games, user_profile],ignore_index=True)
            print(games.iloc[[len(games.index)-1]])
            print('4')
            rec_games_genre = generate_recomendations(games, 'genre')
            print('5')
            rec_games_keywords = generate_recomendations(games, 'summary')
            print('6')
            success =  True
            recs = []
            recs.extend(rec_games_genre[:10])
            recs.extend(rec_games_keywords[:20])
            print('7')
            [rec_games.append(game) for game in recs if game not in rec_games]
            rec_games = rec_games[:20]
        return JsonResponse ({
                'games_list' : rec_games,
                'success' : success,
            })
def generate_non_rec_list(curr_user_id):
    non_rec_list = []
    play_list = pd.DataFrame.from_records(PlayList.objects.filter(user_id = curr_user_id).values())
    dislike_list = pd.DataFrame.from_records(DislikeList.objects.filter(user_id = curr_user_id).values())
    completed_list = pd.DataFrame.from_records(CompletedList.objects.filter(user_id = curr_user_id).values())
    if not play_list.empty:
        [non_rec_list.append(game) for game in play_list['play_list_game'] if game not in non_rec_list ]
    if not dislike_list.empty:
        [non_rec_list.append(game) for game in dislike_list['dislike_list_game'] if game not in non_rec_list ]
    if not completed_list.empty:
        [non_rec_list.append(game) for game in completed_list['completed_list_game'] if game not in non_rec_list ]
    print( non_rec_list)
    return non_rec_list

def filter_list(filter_items):
    if(len(filter_items)>0):
        query = Game.objects.all()
        for item in filter_items:
            query = query.exclude(title = item)
    else:
        query = Game.objects.all()

    return pd.DataFrame.from_records(query.values())



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
        #print(overview_matrix.shape)
        similarity_matrix = linear_kernel(overview_matrix,overview_matrix)
        mapping = pd.Series(games.index, index = games['title'])
        user_index = mapping["user_profile_temp"]
        similarity_score = list(enumerate(similarity_matrix[user_index]))
        similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
        similarity_score = similarity_score[1:200]
        games_index = [i[0] for i in similarity_score]
        #print(games['title'].iloc[games_index])
        rec_games = []
        [rec_games.append(game) for game in games['title'].iloc[games_index] if game not in rec_games ]
        if 'user_profile_temp' in rec_games:
            rec_games.remove('user_profile_temp')
        return rec_games

def add_keywords(title, curr_user_id):
    keywords = get_keywords(title)
    if(Profile.objects.filter(user_id=curr_user_id).exists()):
        player_profile = Profile.objects.get(user_id=curr_user_id)
        current_keywords = player_profile.keyword
        new_keywords = []
        new_keywords= re.findall(r'\w+', current_keywords)
        [new_keywords.append(keyword) for keyword in keywords if keyword not in new_keywords ]
        player_profile.keyword = new_keywords
        player_profile.save()


def remove_keywords(title, curr_user_id):
    keywords = get_keywords(title)
    if(Profile.objects.filter(user_id=curr_user_id).exists()):
        player_profile = Profile.objects.get(user_id=curr_user_id)
        current_keywords = re.findall(r'\w+', player_profile.keyword)
        [current_keywords.remove(keyword) for keyword in keywords if keyword in current_keywords]    
        player_profile.keyword =  current_keywords
        player_profile.save()

def add_genres(game_title, curr_user_id):
    if(Profile.objects.filter(user_id=curr_user_id).exists()):
        player_profile = Profile.objects.get(user_id=curr_user_id)
        genres = re.findall(r'\w+', player_profile.genre)
        query = Game.objects.all().filter(title = game_title).values()
        df = pd.DataFrame.from_records(query)
        genres.extend((df['genre'].iloc[0]).split(", "))
        player_profile.genre = genres
        player_profile.save()

def remove_genres(game_title, curr_user_id):
    if(Profile.objects.filter(user_id=curr_user_id).exists()):
        player_profile = Profile.objects.get(user_id=curr_user_id)
        genres = re.findall(r'\w+', player_profile.genre)
        query = Game.objects.all().filter(title = game_title).values()
        df = pd.DataFrame.from_records(query)
        to_remove_genres = (df['genre'].iloc[0]).split(", ")
        [genres.remove(genre) for genre in to_remove_genres if genre in genres]    
        player_profile.genre = genres
        player_profile.save()
        
@csrf_exempt
def like_game(request: HttpRequest) -> JsonResponse:
    success = False
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if (data['liked_game']!=""):
            if(PlayList.objects.filter(user_id = data['user_id'], play_list_game = data['liked_game']).exists() == False):
                play_list_entry = PlayList.objects.create(
                    play_list_game = data['liked_game'],
                    user_id = data['user_id'],
                )
                add_keywords(data['liked_game'],data['user_id'])
                add_genres(data['liked_game'],data['user_id'])
            return JsonResponse({
                'success': success
            })
        
def get_user_liked(request: HttpRequest) -> JsonResponse:
    success = False
    if request.method == 'GET':
        curr_user_id = json.loads(request.session.__getitem__("_auth_user_id"))
        liked_games = []
        if (PlayList.objects.filter(user_id=curr_user_id).exists()):
            play_list = pd.DataFrame.from_records(PlayList.objects.filter(user_id = curr_user_id).values())
            if not play_list.empty:
                [liked_games.append(game) for game in play_list['play_list_game'] if game not in liked_games ]
        return JsonResponse ({
                'games_list' : liked_games,
                'success' : success,
            })
        
@csrf_exempt
def dislike_game(request: HttpRequest) -> JsonResponse:
    success = False
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if (data['disliked_game']!=""):
            if(DislikeList.objects.filter(user_id = data['user_id'], dislike_list_game = data['disliked_game']).exists() == False):
                dislike_list_entry = DislikeList.objects.create(
                    dislike_list_game = data['disliked_game'],
                    user_id = data['user_id'],
                )
                remove_keywords(data['disliked_game'],data['user_id'])
                remove_genres(data['disliked_game'],data['user_id'])
            return JsonResponse({
                'success': success
            })
    
def get_user_disliked(request: HttpRequest) -> JsonResponse:
    success = False
    if request.method == 'GET':
        curr_user_id = json.loads(request.session.__getitem__("_auth_user_id"))
        disliked_games = []
        if (DislikeList.objects.filter(user_id=curr_user_id).exists()):
            dislike_list = pd.DataFrame.from_records(DislikeList.objects.filter(user_id = curr_user_id).values())
            if not dislike_list.empty:
                [disliked_games.append(game) for game in dislike_list['dislike_list_game'] if game not in disliked_games ]
        return JsonResponse ({
                'games_list' : disliked_games,
                'success' : success,
            })
    

@csrf_exempt
def completed_game(request: HttpRequest) -> JsonResponse:
    success = False
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if (data['completed_game']!=""):
            if(CompletedList.objects.filter(user_id = data['user_id'], completed_list_game = data['completed_game']).exists() == False):
                completed_list_entry = CompletedList.objects.create(
                    completed_list_game = data['completed_game'],
                    user_id = data['user_id'],
                )
                add_keywords(data['completed_game'],data['user_id'])
                add_genres(data['completed_game'],data['user_id'])
            return JsonResponse({
                'success': success
            })
        
def get_user_completed(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        curr_user_id = json.loads(request.session.__getitem__("_auth_user_id"))
        completed_games = []
        if (CompletedList.objects.filter(user_id=curr_user_id).exists()):
            completed_list = pd.DataFrame.from_records(CompletedList.objects.filter(user_id = curr_user_id).values())
            if not completed_list.empty:
                [completed_games.append(game) for game in completed_list['completed_list_game'] if game not in completed_games ]
        return JsonResponse ({
                'games_list' : completed_games,
            })
    

@csrf_exempt
def remove_list_game(request: HttpRequest) -> JsonResponse:
    success = False
    if request.method == 'DELETE':
        data = json.loads(request.body.decode('utf-8'))
        if (data['curr_list'] == 'completed'):
            game = CompletedList.objects.filter(user_id = data['user_id'], completed_list_game = data['game_to_remove'])
        elif (data['curr_list'] == 'disliked'):
            game = DislikeList.objects.filter(user_id = data['user_id'], dislike_list_game = data['game_to_remove'])
        else:
            game = PlayList.objects.filter(user_id = data['user_id'], play_list_game = data['game_to_remove'])
            
        game.delete()
        success = True
        return JsonResponse ({
                'success' : success,
            })
    
def get_game_data(request: HttpRequest, curr_title: str) -> JsonResponse:
    success = False
    if request.method == 'GET':
        curr_game_data = {}
        if (Game.objects.filter(title=curr_title).exists()):
            curr_game_data  = Game.objects.filter(title=curr_title).first().to_dict()
            platforms = list(Game.objects.filter(title=curr_title).values_list('platforms', flat=True))
            curr_game_data ['platforms'] = ', '.join(platforms)
        return JsonResponse({
            'games': curr_game_data  
            })
@csrf_exempt
def profile(request: HttpRequest) -> JsonResponse:
    success = False
    error_msg = ''
    if request.method == 'GET':
        curr_user_id = json.loads(request.session.__getitem__("_auth_user_id"))
        user = {}
        if (MyUser.objects.filter(id=curr_user_id).exists()):
            user = MyUser.objects.get(id=curr_user_id).to_dict()
        return JsonResponse({
            'user': user  
            })
    elif request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        if (MyUser.objects.filter(id=data['user_id']).exists()):
            curr_user = MyUser.objects.get(id=data['user_id'])
            if 'first_name' in data:
                if data['first_name'].strip():
                    curr_user.first_name = data['first_name']
            if 'surname' in data:
                if data['surname'].strip():
                    curr_user.last_name = data['surname']
            if 'username' in data:
                if ((data['username']).strip()):
                    if(MyUser.objects.filter(username=data['username']).exists()):
                        success = False
                        error_msg = "This username already exists!"
                    else:
                        curr_user.username = data['username']
            if 'email' in data:
                if data['email'].strip():
                    curr_user.email = data['email']
            if 'date_of_birth' in data:
                if data['date_of_birth'].strip():
                    curr_user.date_of_birth = data['date_of_birth']

            curr_user.save()
            success = True
        return JsonResponse({
            'success': success,
            'error_msg' : error_msg
            })    
    
def home_page(request: HttpRequest) -> JsonResponse:
    success = False
    error_msg = ''
    if request.method == 'GET':
        curr_user_id = json.loads(request.session.__getitem__("_auth_user_id"))
        top_genre = ''
        play_list_overview = []
        completed_list_overview = []
        name = ''
        if (MyUser.objects.filter(id=curr_user_id).exists()):
            name = MyUser.objects.get(id=curr_user_id).first_name
            if (Profile.objects.filter(user_id=curr_user_id).exists()):
                player_profile = Profile.objects.get(user_id=curr_user_id)
                genres = re.findall(r'\w+', player_profile.genre)
                counter = Counter(genres)
                top_genre = counter.most_common(1)[0][0]
            play_list = pd.DataFrame.from_records(PlayList.objects.filter(user_id = curr_user_id).values())
            completed_list = pd.DataFrame.from_records(CompletedList.objects.filter(user_id = curr_user_id).values())
            play_list_items = []
            completed_list_items = []
            if not play_list.empty:
                [play_list_items.append(game) for game in play_list['play_list_game'] if game not in play_list_items ]
                play_list_overview = random.choices(play_list_items, k=5)
            if not completed_list.empty:
                [completed_list_items.append(game) for game in completed_list['completed_list_game'] if game not in completed_list_items ]
                completed_list_overview = random.choices(completed_list_items, k=5)

    return JsonResponse({
        'play_overview': play_list_overview,
        'completed_overview' : completed_list_overview, 
        'top_genre' : top_genre,
        'user_name' : name,
        })    

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