from importlib import import_module
from django.test import TestCase, RequestFactory
from django.test import Client
from .models import MyUser, Profile,PlayList,DislikeList,CompletedList
from django.urls import reverse
from django.conf import settings
from . import views

# Create your tests here.
class ViewTests(TestCase):

    def setUp(self):
        test_username = 'testacc'
        test_password = 'Testing123'
        test_email = 'test@testmail.com'
        client = Client()
        MyUser.objects.create(username = test_username, email = test_email, password = test_password)
        self.client.get(reverse('load DB'))
        self.factory = RequestFactory()


    def test_log_in(self):
        test_username = 'testacc'
        test_password = 'Testing123'
        test_email = 'test@testmail.com'
        client = Client()
        response = client.post(reverse('Login'), {'username':test_username, 'password':test_password})
        self.assertEqual(response.status_code,302)

    def test_sign_up(self):
        test_fname = 'test'
        test_lname = 'account'
        test_username = 'testacc'
        test_password = 'Testing123'
        test_email = 'test@testmail.com'
        test_dob = '1970-01-01'
        client = Client()
        response = client.post(reverse('SignUp'), {'first_name':test_fname,'last_name':test_lname,'username':test_username,'email':test_email, 'date_of_birth':test_dob, 'password1':test_password,'password2':test_password})
        self.assertEqual(response.status_code,200)
    
    def test_temp_profile(self):
        client = Client()
        test_items = ["Coop","Role-Playing; Action RPG; Action","Puzzle; Turn-Based","Action Adventure; Open-World"]
        test_id = MyUser.objects.all()[0].id
        response = client.post(reverse('Store Temp Profile'), {"user_id":test_id,"picked_items":test_items},content_type="application/json")
        self.assertEqual(response.status_code,200)
        self.assertEqual(Profile.objects.count(),1)

    def test_store_profile(self):
        client = Client()
        test_items = ["The Legend of Zelda: Breath of the Wild","Horizon Forbidden West"]
        test_id = MyUser.objects.all()[0].id
        response = client.post(reverse('Store Profile'), {'user_id':test_id,'games_choice':test_items},content_type="application/json")
        self.assertEqual(response.status_code,200)

    def test_quiz_games(self):
        test_genres = ['Story', 'Role-Playing', 'Action RPG', 'Console-style RPG', 'Fantasy']
        test_num_players ='Coop'
        test_id = MyUser.objects.all()[0].id
        Profile.objects.create(keyword = '', genre=test_genres, num_players_preference=test_num_players, user_id =test_id )
        request = self.factory.get(reverse('Get Quiz Games'))
        request.session = {'_auth_user_id': str(test_id)}
        response = views.get_quiz_games(request)
        self.assertEqual(response.status_code,200)


    def test_get_questions(self):
        client = Client()
        response = client.get(reverse('Get Questions'))
        self.assertEqual(response.status_code,200)

    def test_user_recommendations(self):
        test_genres = ['braves', 'thugs', 'undefeatable', 'elixirs', 'warmer', 'hormone',]
        test_num_players ='Coop'
        test_id = MyUser.objects.all()[0].id
        Profile.objects.create(keyword = '', genre=test_genres, num_players_preference=test_num_players, user_id =test_id )
        request = self.factory.get(reverse('User Recommendations'))
        request.session = {'_auth_user_id': str(test_id)}
        response = views.user_recommendations(request)
        self.assertEqual(response.status_code,200)
        
    def test_like_game(self):
        client = Client()
        test_items = "The Legend of Zelda: Breath of the Wild"
        test_id = MyUser.objects.all()[0].id
        response = client.post(reverse('Like Game'), {'user_id':test_id,'liked_game':test_items},content_type="application/json")
        self.assertEqual(response.status_code,200)
        self.assertEqual(PlayList.objects.count(),1)
    
    def test_complete_game(self):
        client = Client()
        test_items = "The Legend of Zelda: Breath of the Wild"
        test_id = MyUser.objects.all()[0].id
        response = client.post(reverse('Completed Game'), {'user_id':test_id,'completed_game':test_items},content_type="application/json")
        self.assertEqual(response.status_code,200)
        self.assertEqual(CompletedList.objects.count(),1)

    def test_dislike_game(self):
        client = Client()
        test_items = "Resident Evil 4: Wii Edition"
        test_id = MyUser.objects.all()[0].id
        response = client.post(reverse('Dislike Game'), {'user_id':test_id,'disliked_game':test_items},content_type="application/json")
        self.assertEqual(response.status_code,200)
        self.assertEqual(DislikeList.objects.count(),1)

    def test_remove_game(self):
        client = Client()
        test_items = "The Legend of Zelda: Breath of the Wild"
        test_id = MyUser.objects.all()[0].id
        response = client.post(reverse('Dislike Game'), {'user_id':test_id,'disliked_game':test_items},content_type="application/json")
        response = client.delete(reverse('Remove List Game'), {'user_id':test_id,'curr_list':'disliked','game_to_remove':test_items},content_type="application/json")
        self.assertEqual(response.status_code,200)
        self.assertEqual(DislikeList.objects.count(),0)

    def test_get_profile(self):
        test_id = MyUser.objects.all()[0].id
        request = self.factory.get(reverse('Profile API'))
        request.session = {'_auth_user_id': str(test_id)}
        response = views.profile(request)
        self.assertEqual(response.status_code,200)

    def test_edit_profile(self):
        client = Client()
        test_name = "testuser123"
        test_id = MyUser.objects.all()[0].id
        response = client.put(reverse('Profile API'), {'user_id':test_id,'first_name':test_name},content_type="application/json")
        self.assertEqual(response.status_code,200)

    def test_home_page(self):
        test_id = MyUser.objects.all()[0].id
        request = self.factory.get(reverse('Home Page'))
        request.session = {'_auth_user_id': str(test_id)}
        response = views.home_page(request)
        self.assertEqual(response.status_code,200)


