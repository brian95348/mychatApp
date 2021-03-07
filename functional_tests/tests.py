
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from django.urls import reverse
from django.contrib.auth import get_user_model
from chat.models import Profile, Message

User = get_user_model()
class TestProjectPage(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.User1       = User.objects.create_user(username='user1',password='1234',email='user1@user.com')
        cls.User2       = User.objects.create_user(username='user2',password='1234',email='user2@user.com')
        cls.User3       = User.objects.create_user(username='user3',password='1234',email='user3@user.com')
        cls.Profile1    = Profile.objects.create(user=cls.User1, status='profile for user1') 
        cls.Profile2    = Profile.objects.create(user=cls.User2, status='profile for user2')
        cls.message1    = Message.objects.create(user=cls.User1,text='user1 to user2',receiver=cls.User2.username)
        cls.message2    = Message.objects.create(user=cls.User2,text='user2 to user1',receiver=cls.User1.username)
        cls.selenium    = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        
        super().tearDownClass()

     
    def login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('user1')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('1234')
        self.selenium.find_element_by_xpath('//input[@value="Login"]').click() 

    def test_chat_list(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/chat/chatlist/'))
        self.login()

    def test_profile_detail(self):
        #Viewing User2 Profile object
        self.selenium.get(self.live_server_url+reverse('profile-detail',kwargs={'username':self.User2.username}))
        self.login()
