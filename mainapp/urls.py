from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="Login"),
    path('sign-up', views.signup, name='SignUp'),
    path('ses-user', views.get_user, name="Get UserID"),
    path('getQuestions', views.get_questions, name="Get Questions"),
    path('storeTempProfile', views.store_temp_profile, name="Store Temp Profile"),
]