from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="Login"),
    path('sign-up', views.signup, name='SignUp'),
    path('ses-user', views.get_user, name="Get UserID"),
    path('get-questions', views.get_questions, name="Get Questions"),
    path('store-temp-profile', views.store_temp_profile, name="Store Temp Profile"),
    path('load-db',views.load_db, name="load DB"),
    path('get-quiz-games',views.get_quiz_games, name="Get Quiz Games"),
    path('store-profile', views.store_profile, name="Store Profile"),
    path('user-recommendations', views.user_recommendations, name="User Recommendations"),
    
]