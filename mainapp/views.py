from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, authenticate, login
from .forms import LoginForm, SignUpForm
from .models import MyUser, Question, Game, Profile, PlayList, DislikeList, CompletedList, PageView
from django.contrib import messages
from django.contrib.auth import logout
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
from collections import Counter
import json
import re
import random
import os
import pandas as pd

def index(request: HttpRequest):
    """Loads index.html template, used on first load"""
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)
    return render(request, "mainapp/index.html")

def health(request):
    """Takes an request as a parameter and gives the count of pageview objects as reponse"""
    return HttpResponse(PageView.objects.count())

def log_in(request: HttpRequest):
    """Logs in the user using the form from login.html and creates a session, if credentials are correct"""
    if request.method =='POST':
        form = LoginForm(request.POST, request.FILES)
        user = authenticate(username=form['username'].data, password=form['password'].data)
        if user:
            #logs in user if account exists
            login(request, user)
            return render(request,"mainapp/spa/index.html")
        else:
            #otherwise redirects back to log in page and throws error
            messages.error(request,'Incorrect username or password')
            return redirect('./login')
    else:
        form = LoginForm()
        return render(request, "mainapp/login.html",{
            'form' : form,
            'count': PageView.objects.count()
    })

def signup(request: HttpRequest) -> HttpResponse:
    """Allows the user to create an account"""
    success = False
    if (request.method == 'POST'):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your account has been created')
            success = True
        else:
            messages.error(request,'Invalid sign up details')
    form = SignUpForm()
    return render( request, "mainapp/signup.html" , { 
        'form' : form,
        'success' : success,
        } )

def log_out(request):
    """Uses django logout function to destroy user session"""
    logout(request)
    return redirect('./')

def get_user(request: HttpRequest) -> JsonResponse:
    """Returns the session variable _auth_user_id, which stores the current user id"""
    if request.method=='GET':
        return JsonResponse ( {
            'user_id' : request.session.__getitem__("_auth_user_id")
        }, safe=False)

def get_questions(request: HttpRequest) -> JsonResponse:
    """Returns the quiz questions from the table"""
    if request.method == 'GET':
        return JsonResponse (
            [i.to_dict() for i in Question.objects.all()]
         , safe=False)

@csrf_exempt
def store_temp_profile(request: HttpRequest) -> JsonResponse:
    """Stores a temporary profile for the user consisting of genres
    and number of players preference"""
    success = False
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        num_preference = 'All Players'#preference is defaulted to "All Players"
        if (len(data['picked_items']) > 0):
            temp_profile = []
            if (data['picked_items'][0] is not None):
                #first element in list will always be the num_preference
                num_preference = data['picked_items'].pop(0)
            for picked in data['picked_items']:
                if (picked != None):
                    success = True
                    sub_list = picked.split("; ")
                    for item in sub_list:
                        if (item != 'None'):
                            #adds all the genres from the question response to temp profile
                            temp_profile.append(item)
                else:
                    success = False
        if (success == True):
            if(Profile.objects.filter(user_id=data['user_id']).exists()):
                #if profile object exists, then updates object
                player_profile = Profile.objects.get(user_id=data['user_id'])
                player_profile.keyword = ""
                player_profile.genre = temp_profile
                player_profile.num_players_preference = num_preference
                player_profile.save()
            else:
                 #if a profile object doesnt exist, then creates new profile object
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
    """Stores a full profile using the games the user has chosen from the quiz """
    success = False
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if (len(data['games_choice'])>0):
            genres = []
            keywords = []
            #returns word count of all the words
            words = word_count()
            for game in data['games_choice']:
                if(PlayList.objects.filter(user_id = data['user_id'], play_list_game = game).exists() == False):
                    #adds selected game to play list to ensure it is not recommended again
                    play_list_entry = PlayList.objects.create(
                        play_list_game = game,
                        user_id = data['user_id'],
                    )
                query = Game.objects.all().filter(title = game).values()
                df = pd.DataFrame.from_records(query)
                #adds all genres from all the games they chose to a list
                genres.extend((df['genre'].iloc[0]).split(", "))
                #concatenates all keywords to a list with their counts
                keywords.extend(return_keywords(re.findall(r'\w+', df['summary'].iloc[0]), words))
            #sorts and removes any duplicates
            keywords.sort(key = lambda x: x[1])
            cleaned_keywords = []
            [cleaned_keywords.append(kw) for kw in keywords if kw not in cleaned_keywords ]
            profile_keywords = []
            #takes keywords with a count between 2 and 500
            [profile_keywords.append(kw[0]) for kw in cleaned_keywords if kw[1]>1 and kw[1]<501]
            #if a profile exists then it saves the profile, otherwise it passes since profile must be created to be at this step
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
    """Returns the keywords for a specific game with counts between 2 and 100"""
    words = word_count()
    query = Game.objects.all().filter(title = game_title).values()
    df = pd.DataFrame.from_records(query)
    #returns the keywords with the counts
    keywords = return_keywords(re.findall(r'\w+', df['summary'].iloc[0]), words)
    keywords.sort(key = lambda x: x[1])
    cleaned_keywords = []
    [cleaned_keywords.append(kw) for kw in keywords if kw not in cleaned_keywords ]
    profile_keywords = []
    #selects keywords with specified rarity
    [profile_keywords.append(kw[0]) for kw in cleaned_keywords if kw[1]>1 and kw[1]<101]
    return profile_keywords

def word_count():
    """Returns a list of keywords and their counts from all the summaries in the dataset"""
    games = pd.DataFrame.from_records(Game.objects.all().values())
    #uses count vectoriser to count the words
    count_vectoriser = CountVectorizer()
    #constructs the matrix for the count_vectoriser
    words = count_vectoriser.fit_transform(games['summary'])
    #sums all the instances of the words
    count = words.sum(axis=0) 
    #creates an array with format (word, count) for each unique word in the dataset
    frequency = [[word, count[0, i]] for word, i in count_vectoriser.vocabulary_.items()]
    #orders it into rarity order
    frequency =sorted(frequency, key = lambda x: x[1], reverse=True)
    return frequency

def return_keywords(summary, words):
    """Returns keywords for a specified summary"""
    keyword_quantities = []
    for word in summary:
        for keyword in words:
            if word == keyword[0]:
                keyword_quantities.append(keyword)
    return keyword_quantities

        
def get_quiz_games(request: HttpRequest) -> JsonResponse:
    """Uses the recommendation methods to return a list of games for the quiz"""
    success = False
    if request.method == 'GET':
        data = json.loads(request.session.__getitem__("_auth_user_id"))
        if (Profile.objects.filter(user_id=data).exists()):
            #takes the temporary profile from the profiles table
            profile = Profile.objects.get(user_id=data)
            #filters for number of players preference
            games = filter_num_players(profile.get_num_players_preference())
            #uses only genre and creates a user profile dataframe
            user_profile = pd.DataFrame({
                'title': ["user_profile_temp"],
                'genre': [profile.get_genre()]
            })
            games = pd.concat([games, user_profile],ignore_index=True)
            #generates recommendations only using genre 
            rec_games = generate_recomendations(games,user_profile, 'genre')
            success =  True
        return JsonResponse ({
                'games_list' : rec_games,
                'success' : success,
            })
    
def user_recommendations(request: HttpRequest) -> JsonResponse:
    """Returns the main recommendations for a user"""
    success = False
    if request.method == 'GET':
        curr_user_id = json.loads(request.session.__getitem__("_auth_user_id"))
        rec_games = []
        if (Profile.objects.filter(user_id=curr_user_id).exists()):
            profile = Profile.objects.get(user_id=curr_user_id)
            games = filter_num_players(profile.get_num_players_preference())
            non_rec_list = generate_non_rec_list(curr_user_id)
            games = filter_list(non_rec_list)
            user_profile = pd.DataFrame({
                'title': ["user_profile_temp"],
                'genre': [profile.get_genre()],
                'summary': [profile.get_keyword()],
            })
            games = pd.concat([games, user_profile],ignore_index=True)
            rec_games_genre = generate_recomendations(games,user_profile, 'genre')
            rec_games_keywords = generate_recomendations(games,user_profile, 'summary')
            success =  True
            recs = []
            recs.extend(rec_games_genre[:10])
            recs.extend(rec_games_keywords[:20])
            [rec_games.append(game) for game in recs if game not in rec_games]
            rec_games = rec_games[:20]
            random.shuffle(rec_games)
        return JsonResponse ({
                'games_list' : rec_games,
            })
def generate_non_rec_list(curr_user_id):
    """Generates a list of games that are not going to be recommended to the user"""
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
    return non_rec_list

def filter_list(filter_items):
    """Filters the game dataset using a list of items
    to be used with non rec list"""
    if(len(filter_items)>0):
        query = Game.objects.all()
        for item in filter_items:
            query = query.exclude(title = item)
    else:
        query = Game.objects.all()
    return pd.DataFrame.from_records(query.values())

def filter_num_players(num_players_preference):
    """Filters games using the number of players preference"""
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
    #games with a metascore of 75 and over are kept for the sake of speed and simplicity
    query = query.filter(metascore__gte = 75).values()
    return pd.DataFrame.from_records(query)


def generate_recomendations(games, profile, field):
        """Generates recommendations using tf-idf and cosine sim"""
        #creates vectoriser object with english stop words
        tfidf = TfidfVectorizer(stop_words='english')
        #fills all the null fields in the specified column with an empty string
        games[field] = games[field].fillna('')
        #creates the tfidf matrix for the games
        games_tfidf = tfidf.fit_transform(games[field])
        #creates a tfidf matrix for the user profile using the structure of the game matrix
        user_profile_tfidf = tfidf.transform(profile[field])
        #calculates cosine sim using linear_kernel
        cosine_similarity = linear_kernel(user_profile_tfidf, games_tfidf)
        #the results of the cosine similarity are then put into a list and taken in respect to the user profile
        similarity = list(enumerate(cosine_similarity[0]))
        #they are sorted and the top 200 are taken
        similarity = sorted(similarity, key=lambda x: x[1], reverse=True)
        similarity = similarity[1:200]
        recs_index = [i[0] for i in similarity]
        rec_games = []
        #the games are then added and any duplicates are removed
        [rec_games.append(game) for game in games['title'].iloc[recs_index] if game not in rec_games ]
        if 'user_profile_temp' in rec_games:
            rec_games.remove('user_profile_temp')
        return rec_games

def add_keywords(title, curr_user_id):
    """Adds keywords for a specified game and user to the user profile"""
    #extracts keywords from game summary
    keywords = get_keywords(title)
    if(Profile.objects.filter(user_id=curr_user_id).exists()):
        player_profile = Profile.objects.get(user_id=curr_user_id)
        current_keywords = player_profile.keyword
        new_keywords = []
        #appends new kewords list with current keywords
        new_keywords= re.findall(r'\w+', current_keywords)
        #adds the new keywords if they are not already in the keyword list
        [new_keywords.append(keyword) for keyword in keywords if keyword not in new_keywords ]
        #replaces current keywords with an updated keywords list
        player_profile.keyword = new_keywords
        player_profile.save()


def remove_keywords(title, curr_user_id):
    """Removes keywords for a specified game and user from the user profile"""
    keywords = get_keywords(title)
    if(Profile.objects.filter(user_id=curr_user_id).exists()):
        player_profile = Profile.objects.get(user_id=curr_user_id)
        current_keywords = re.findall(r'\w+', player_profile.keyword)
        #removes keywords if they are found in the user profile
        [current_keywords.remove(keyword) for keyword in keywords if keyword in current_keywords]    
        player_profile.keyword =  current_keywords
        player_profile.save()


def add_genres(game_title, curr_user_id):
    """Adds genres for a specified game and user to the user profile"""
    if(Profile.objects.filter(user_id=curr_user_id).exists()):
        player_profile = Profile.objects.get(user_id=curr_user_id)
        genres = re.findall(r'\w+', player_profile.genre)
        #removes unwanted characters from genre
        genres = player_profile.genre.replace("'", '')
        genres = genres.replace("[", '')
        genres = genres.replace("]", '')
        genres = genres.split(",")
        for genre in genres:
            genre = genre.lstrip()
        query = Game.objects.all().filter(title = game_title).values()
        df = pd.DataFrame.from_records(query)
        genres.extend((df['genre'].iloc[0]).split(", "))
        player_profile.genre = genres
        player_profile.save()

def remove_genres(game_title, curr_user_id):
    """Removes genres taken from a specified game and user from the user profile"""
    if(Profile.objects.filter(user_id=curr_user_id).exists()):
        player_profile = Profile.objects.get(user_id=curr_user_id)
        #removes unwanted characters from genre
        genres = player_profile.genre.replace("'", '')
        genres = genres.replace("[", '')
        genres = genres.replace("]", '')
        genres = genres.split(",")
        query = Game.objects.all().filter(title = game_title).values()
        df = pd.DataFrame.from_records(query)
        to_remove_genres = (df['genre'].iloc[0]).split(", ")
        #removes the genres from the genre list stored in the user profile
        [genres.remove(genre) for genre in to_remove_genres if genre in genres]    
        player_profile.genre = genres
        player_profile.save()
        
@csrf_exempt
def like_game(request: HttpRequest) -> JsonResponse:
    """Adds a game to the Play list"""
    success = False
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if (data['liked_game']!=""):
            if(PlayList.objects.filter(user_id = data['user_id'], play_list_game = data['liked_game']).exists() == False):
                #creates a new entry if the game is not in the list already
                play_list_entry = PlayList.objects.create(
                    play_list_game = data['liked_game'],
                    user_id = data['user_id'],
                )
                #adds keywords and genres for that game to the list to develop profile
                add_keywords(data['liked_game'],data['user_id'])
                add_genres(data['liked_game'],data['user_id'])
            return JsonResponse({
                'success': success
            })
        
def get_user_liked(request: HttpRequest) -> JsonResponse:
    """Gets the play list of the user"""
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
    """Adds a game to the dislike list"""
    success = False
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if (data['disliked_game']!=""):
            #creates a new entry if the game is not in the list already
            if(DislikeList.objects.filter(user_id = data['user_id'], dislike_list_game = data['disliked_game']).exists() == False):
                dislike_list_entry = DislikeList.objects.create(
                    dislike_list_game = data['disliked_game'],
                    user_id = data['user_id'],
                )
                #removes keywords and genres for that game from the list to develop profile
                remove_keywords(data['disliked_game'],data['user_id'])
                remove_genres(data['disliked_game'],data['user_id'])
            return JsonResponse({
                'success': success
            })
    
def get_user_disliked(request: HttpRequest) -> JsonResponse:
    """Gets the dislike list of the user"""
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
    """Adds a game to the completed list"""
    success = False
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if (data['completed_game']!=""):
            if(CompletedList.objects.filter(user_id = data['user_id'], completed_list_game = data['completed_game']).exists() == False):
                #creates a new entry if the game is not in the list already
                completed_list_entry = CompletedList.objects.create(
                    completed_list_game = data['completed_game'],
                    user_id = data['user_id'],
                )
                #adds keywords and genres for that game to the list to develop profile
                add_keywords(data['completed_game'],data['user_id'])
                add_genres(data['completed_game'],data['user_id'])
            return JsonResponse({
                'success': success
            })
        
def get_user_completed(request: HttpRequest) -> JsonResponse:
    """Gets the Completed list of the user"""
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
    """Removes a game from a play, completed or dislike list"""
    success = False
    if request.method == 'DELETE':
        data = json.loads(request.body.decode('utf-8'))
        #checks what list the game is specified for and removes it from that list.
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
    """Returns the metadata for a game to be viewed"""
    success = False
    if request.method == 'GET':
        curr_game_data = {}
        if (Game.objects.filter(title=curr_title).exists()):
            curr_game_data  = Game.objects.filter(title=curr_title).first().to_dict()
            #extracts all the platforms for the game and creates a list of platforms
            platforms = list(Game.objects.filter(title=curr_title).values_list('platforms', flat=True))
            curr_game_data ['platforms'] = ', '.join(platforms)
        return JsonResponse({
            'games': curr_game_data  
            })
    
@csrf_exempt
def profile(request: HttpRequest) -> JsonResponse:
    """Handles profile updates and viewing"""
    success = False
    error_msg = ''
    if request.method == 'GET':
        curr_user_id = json.loads(request.session.__getitem__("_auth_user_id"))
        user = {}
        if (MyUser.objects.filter(id=curr_user_id).exists()):
            #returns the user object on a GET request
            user = MyUser.objects.get(id=curr_user_id).to_dict()
        return JsonResponse({
            'user': user  
            })
    elif request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        if (MyUser.objects.filter(id=data['user_id']).exists()):
            curr_user = MyUser.objects.get(id=data['user_id'])
            #changes the database record and saves the user record if the user has chosen to change a field
            if 'first_name' in data:
                if data['first_name'].strip():
                    curr_user.first_name = data['first_name']
            if 'surname' in data:
                if data['surname'].strip():
                    curr_user.last_name = data['surname']
            if 'username' in data:
                if ((data['username']).strip()):
                    #checks if username exists in database and returns error message if it is the case
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
    """Returns home page lists to be used on the home page"""
    if request.method == 'GET':
        curr_user_id = json.loads(request.session.__getitem__("_auth_user_id"))
        #initialise empty variables
        top_genre = ''
        play_list_overview = []
        completed_list_overview = []
        name = ''
        if (MyUser.objects.filter(id=curr_user_id).exists()):
            name = MyUser.objects.get(id=curr_user_id).first_name
            #extracting genres from profile
            if (Profile.objects.filter(user_id=curr_user_id).exists()):
                player_profile = Profile.objects.get(user_id=curr_user_id)
                genres = player_profile.genre.replace("'", '')
                genres = genres.replace("[", '')
                genres = genres.replace("]", '')
                genres = genres.split(",")
                #return the top genre from the list of genres
                counter = Counter(genres)
                top_genre = counter.most_common(1)[0][0]
            #retrieve all data for current user in play list and completed list
            play_list = pd.DataFrame.from_records(PlayList.objects.filter(user_id = curr_user_id).values())
            completed_list = pd.DataFrame.from_records(CompletedList.objects.filter(user_id = curr_user_id).values())
            play_list_items = []
            completed_list_items = []
            #store up to 5 random games to be displayed on the home page from each list
            if not play_list.empty:
                [play_list_items.append(game) for game in play_list['play_list_game'] if game not in play_list_items ]
                if (len(play_list_items) < 5):
                    play_list_overview = random.sample(play_list_items, len(play_list_items))
                else:
                    play_list_overview = random.sample(play_list_items, 5)
            if not completed_list.empty:
                [completed_list_items.append(game) for game in completed_list['completed_list_game'] if game not in completed_list_items ]
                if (len(completed_list_items) < 5):
                    completed_list_overview = random.sample(completed_list_items, len(completed_list_items))
                else:
                    completed_list_overview = random.sample(completed_list_items, 5)
    return JsonResponse({
        'play_overview': play_list_overview,
        'completed_overview' : completed_list_overview, 
        'top_genre' : top_genre,
        'user_name' : name,
        })    

def load_db(request: HttpRequest) -> HttpResponse:
    """Loads the game dataset into the database using the file from the public github repository"""
    games = pd.read_csv('https://raw.githubusercontent.com/aadamhuda/VideoGamesRecommendationSystem/main/mainapp/static/metacritic_games_master.csv')
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