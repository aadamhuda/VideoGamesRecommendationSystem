from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    date_of_birth = models.DateField(default='1970-01-01')
    genres = models.TextField(default="")
    keywords = models.TextField(default="")

    def getDOB(self):
        return self.date_of_birth

    def getGenres(self):
        return self.genres

    def getKeywords(self):
        return self.keywords

    
    def to_dict(self):
        return {
            'username': self.username,
            'password' : self.password,
            'email' : self.email,
            'dateOfBirth' : self.date_of_birth,
            'genres' : self.genres,
            'keywords' : self.keywords
        }
