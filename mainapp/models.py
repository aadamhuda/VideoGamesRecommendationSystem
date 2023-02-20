from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    date_of_birth = models.DateField(default='1970-01-01')

    def getDOB(self):
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

    def getQuestion(self):
        return self.question_text

    def getStronglyAgree(self):
        return self.strongly_agree

    def getAgree(self):
        return self.agree

    def getNeither(self):
        return self.neither

    def getDisagree(self):
        return self.disagree

    def getStronglyDisagree(self):
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

class Genres(models.Model):
    genre = models.CharField(max_length=50)
    user_id = models.IntegerField()
    weight = models.DecimalField(decimal_places=3, max_digits=4)

    def getGenre(self):
        return self.genre

    def getUserID(self):
        return self.user_id
    
    def getWeight(self):
        return self.weight

    def to_dict(self):
        return {
            'genre_id' : self.id,
            'genre' : self.genre,
            'user_id' : self.user_id,
            'weight' : self.weight,
        }

class Keywords(models.Model):
    keyword = models.CharField(max_length=50)
    user_id = models.IntegerField()
    weight = models.DecimalField(decimal_places=3, max_digits=4)

    def getKeyword(self):
        return self.keyword

    def getUserID(self):
        return self.user_id

    def getWeight(self):
        return self.weight

    def to_dict(self):
        return {
            'keyword_id' : self.id,
            'keyword' : self.keyword,
            'user_id' : self.user_id,
            'weight' : self.weight,
        }


class TempProfile(models.Model):
    keyword = models.CharField(max_length=50)
    user_id = models.IntegerField()
    weight = models.DecimalField(decimal_places=3, max_digits=4)

    def getKeyword(self):
        return self.keyword

    def getUserID(self):
        return self.user_id

    def getWeight(self):
        return self.weight

    def to_dict(self):
        return {
            'keyword_id' : self.id,
            'keyword' : self.keyword,
            'user_id' : self.user_id,
            'weight' : self.weight,
        }
