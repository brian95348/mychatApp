from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import get_user_model
from .models import Profile, Message
from django.urls import reverse
from .views import ProfileListView, ProfileDetailView, ProfileDeleteView
from .forms import ProfileModelForm
import datetime

User = get_user_model()
class ViewsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.User1       = User.objects.create_user(username='user1',password='1234',email='user1@user.com')
        cls.User2       = User.objects.create_user(username='user2',password='1234',email='user2@user.com')
        cls.Profile1    = Profile.objects.create(user=cls.User1, status='profile for user1') 
        cls.Profile2    = Profile.objects.create(user=cls.User2, status='profile for user2')
        cls.update_url = reverse('profile-update',kwargs={'username':cls.Profile1.username})

    def setUp(self):
        self.client.login(username=self.User1,password='1234')
        
    def test_profile_list_view_get(self):
        list_url    = reverse('profile-list')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'chat/profile_list.html')
 
    def test_profile_detail_view(self):
        detail_url = reverse('profile-detail',kwargs={'username':cls.Profile2.username})
        response = self.client.get(detail_url)
        self.assertTemplateUsed(response,'chat/profile_detail.html')
        self.assertEqual(response.status_code,200)

    def test_profile_update_view_get(self):
        response = self.client.get(self.update_url)
        self.assertTemplateUsed(response,'chat/profile_updateform.html')
        self.assertEqual(response.status_code,200)

    def test_profile_update_view_post(self):
        response = self.client.post(self.update_url,{
            'user':self.User1,
            'status':'status changed'
        })
        self.assertEqual(response.status_code,302)

    def test_profile_delete_view(self):
        delete_url = reverse('profile-delete',kwargs={'username':cls.Profile1.username})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code,302) 

class FormsTest(TestCase):

    def test_form_with_no_data(self):
        form = ProfileModelForm()
        self.assertFalse(form.is_valid())

    def test_form_with_valid_data(self):
        user = User.objects.create_user(username='user1',password='1234',email='user1@user.com')
        form = ProfileModelForm(data={
            'user': user,
            'status': 'hey there'
        })
        self.assertTrue(form.is_valid())
