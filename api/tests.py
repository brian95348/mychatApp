from rest_framework.test import APITestCase
from django.urls import reverse
from .views import ProfileList, ProfileCreate, ProfileDetail
from chat.models import Message, Profile
from django.contrib.auth import get_user_model
from rest_framework import status
from .serializers import MessageSerializer, ProfileSerializer

User = get_user_model()

class APIViewsTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.User1       = User.objects.create_user(username='user1',password='1234',email='user1@user.com')
        cls.User2       = User.objects.create_user(username='user2',password='1234',email='user2@user.com')
        cls.User3       = User.objects.create_user(username='user3',password='1234',email='user3@user.com')
        cls.Profile1    = Profile.objects.create(user=cls.User1, status='profile for user1') 
        cls.Profile2    = Profile.objects.create(user=cls.User2, status='profile for user2')
        cls.message1    = Message.objects.create(user=cls.User1,text='user1 to user2',receiver=cls.User2.username)
        cls.message2    = Message.objects.create(user=cls.User2,text='user2 to user1',receiver=cls.User1.username)
        cls.profile_update_url = reverse('api-profile-detail',kwargs={'username':cls.Profile1.username})
  
    def test_profile_list_view_get(self):
        chatlist_url    = reverse('api-chats')
        self.client.force_authenticate(user=self.User1)
        response = self.client.get(chatlist_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
         
    def test_profile_detail_view(self):
        profile_detail_url = reverse('api-profile-detail',kwargs={'username':self.Profile2.username})
        self.client.force_authenticate(user=self.User1)
        response = self.client.get(profile_detail_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_profile_update_view(self):
        self.client.force_authenticate(user=self.User1)
        response = self.client.patch(self.profile_update_url,{
            'status':'status changed'
            })
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_profile_delete_view(self):
        self.client.force_authenticate(user=self.User1)
        response = self.client.delete(self.profile_update_url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertEqual(Profile.objects.count(),1)

    def test_profile_create_view(self):
        self.client.force_authenticate(user=self.User3)
        profile_create_url = reverse('api-profile-create')
        response = self.client.post(profile_create_url,{
            'status':'user3'
            }, format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Profile.objects.count(),3)

    def test_chat_view(self):
        self.client.force_authenticate(user=self.User1)
        chat_url = reverse('api-chat',kwargs={'username':self.Profile2.username})
        response = self.client.get(chat_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_chat_create(self):
        self.client.force_authenticate(user=self.User1)
        chat_url = reverse('api-chat',kwargs={'username':self.Profile2.username})
        response = self.client.post(chat_url,{
                    'text':'message',
            }, format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_chat_message_detail_view(self):
        self.client.force_authenticate(user=self.User1)
        chat_message_url = reverse('api-chat-message',kwargs={'username':self.Profile2.username, 'pk':self.message1.id})
        response = self.client.get(chat_message_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_chat_message_delete(self):
        self.client.force_authenticate(user=self.User1)
        chat_message_url = reverse('api-chat-message',kwargs={'username':self.Profile2.username, 'pk':self.message2.id})
        response = self.client.delete(chat_message_url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_user_signup(self):
        user_signup_url = reverse('api-user-signup')
        response = self.client.post(user_signup_url,{'username':'Bra',
            'password':'12345678',
            'email':'bfzulu95@gmail.com'}, format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
       

class APISerializersTests(APITestCase):
     
    def test_message_serializer_with_data(self):
         serializer = MessageSerializer(data={
            "text":"test message",
            "receiver": "brian"
            })
         self.assertTrue(serializer.is_valid())

    def test_profile_serializer_with_data(self):
         serializer = ProfileSerializer(data={
            "username":"brian",
            "status": "hey there"
            })
         self.assertTrue(serializer.is_valid())

