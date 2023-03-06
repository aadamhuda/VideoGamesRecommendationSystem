from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    date_of_birth = models.DateField(default='1970-01-01')

    def get_dob(self):
        return self.date_of_birth
    
    def to_dict(self):
        return {
            'username': self.username,
            'password' : self.password,
            'email' : self.email,
            'dateOfBirth' : self.date_of_birth,
        }

class Question(models.Model):
    question_text = models.CharField(max_length=500)
    strongly_agree = models.CharField(max_length=100)
    agree = models.CharField(max_length=100)
    neither = models.CharField(max_length=100)
    disagree = models.CharField(max_length=100)
    strongly_disagree = models.CharField(max_length=100)

    def __str__(self):
        return self.question_text

    def get_question(self):
        return self.question_text

    def get_strongly_agree(self):
        return self.strongly_agree

    def get_agree(self):
        return self.agree

    def get_neither(self):
        return self.neither

    def get_disagree(self):
        return self.disagree

    def get_strongly_disagree(self):
        return self.strongly_disagree

    def to_dict(self):
        return {
            'question_id' : self.id,
            'question_text' : self.question_text,
            'strongly_agree' : self.strongly_agree,
            'agree' : self.agree,
            'neither' : self.neither,
            'disagree' : self.disagree,
            'strongly_disagree' : self.strongly_disagree,
        }

class Profile(models.Model):
    keyword = models.TextField()
    genre = models.TextField()
    num_players_preference = models.CharField(max_length=50)
    user_id = models.IntegerField()

    def get_keyword(self):
        return self.keyword

    def get_genre(self):
        return self.genre

    def get_num_players_preference(self):
        return self.num_players_preference

    def get_user_id(self):
        return self.user_id

    def to_dict(self):
        return {
            'profile_id' : self.id,
            'keyword' : self.keyword,
            'genre' : self.genre,
            'num_players_preference' : self.num_players_preference,
            'user_id' : self.user_id,
        }
    
class PlayList(models.Model):
    play_list_game = models.CharField(max_length=100)
    user_id = models.IntegerField()

    def get_keyword(self):
        return self.play_list_game

    def get_user_id(self):
        return self.user_id

    def to_dict(self):
        return {
            'play_list_id' : self.id,
            'play_list_game' : self.play_list_game,
            'user_id' : self.user_id,
        }
    
class CompletedList(models.Model):
    completed_list_game = models.CharField(max_length=100)
    user_id = models.IntegerField()

    def get_keyword(self):
        return self.completed_list_game

    def get_user_id(self):
        return self.user_id

    def to_dict(self):
        return {
            'completed_list_id' : self.id,
            'completed_list_game' : self.completed_list_game,
            'user_id' : self.user_id,
        }
    
class DislikeList(models.Model):
    dislike_list_game = models.CharField(max_length=100)
    user_id = models.IntegerField()

    def get_keyword(self):
        return self.dislike_list_game

    def get_user_id(self):
        return self.user_id

    def to_dict(self):
        return {
            'dislike_list_id' : self.id,
            'dislike_list_game' : self.dislike_list_game,
            'user_id' : self.user_id,
        }



class Game(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.CharField(max_length=50)
    genre = models.CharField(max_length=200)
    platforms = models.CharField(max_length=50)
    developer = models.CharField(max_length=50)
    esrb_rating = models.CharField(max_length=50)
    esrbs = models.CharField(max_length=100)
    metascore = models.IntegerField()
    userscore = models.CharField(max_length=50)
    num_players = models.CharField(max_length=50)
    summary = models.TextField()

    def __str__(self):
        return self.title

    def get_title(self):
        return self.title
    
    def get_release_date(self):
        return self.release_date

    def get_genre(self):
        return self.genre

    def get_platforms(self):
        return self.platforms

    def get_developer(self):
        return self.developer

    def get_esrb_rating(self):
        return self.esrb_rating

    def get_esrbs(self):
        return self.esrbs

    def get_metascore(self):
        return self.metascore

    def get_userscore(self):
        return self.userscore

    def get_num_players(self):
        return self.num_players

    def get_summary(self):
        return self.summary

    def to_dict(self):
        return {
            'game_id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'genre': self.genre,
            'platforms': self.platforms,
            'developer': self.developer,
            'esrb_rating': self.esrb_rating,
            'esrbs': self.esrbs,
            'metascore': self.metascore,
            'userscore': self.userscore,
            'num_players': self.num_players,
            'summary': self.summary,
        }