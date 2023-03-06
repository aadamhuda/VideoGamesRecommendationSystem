from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="Login"),
    path('logout', views.log_out, name="Logout"),
    path('sign-up', views.signup, name='SignUp'),
    path('ses-user', views.get_user, name="Get UserID"),
    path('get-questions', views.get_questions, name="Get Questions"),
    path('store-temp-profile', views.store_temp_profile, name="Store Temp Profile"),
    path('load-db',views.load_db, name="load DB"),
    path('get-quiz-games',views.get_quiz_games, name="Get Quiz Games"),
    path('store-profile', views.store_profile, name="Store Profile"),
    path('user-recommendations', views.user_recommendations, name="User Recommendations"),
    path('like-game', views.like_game, name="Like Game"),
    path('dislike-game', views.dislike_game, name="Dislike Game"),
    path('completed-game', views.completed_game, name="Completed Game"),
    path('get-user-liked', views.get_user_liked, name="Get User Liked"),
    path('get-user-disliked', views.get_user_disliked, name="Get User Disiked"),
    path('get-user-completed', views.get_user_completed, name="Get User Completed"),
    path('remove-list-game', views.remove_list_game, name="Remove List Game"),
    path('get-game-data/<str:curr_title>', views.get_game_data, name='Get Game Data'),
    path('user-profile', views.profile, name='Profile API')
]