from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, UserManager
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from guardian.shortcuts import assign_perm
from rest_framework.authtoken.models import Token
# Create your models here.

def uploadedfile_path(instance, filename):
    return 'profiles/{}_{}/{}'.format(instance.user.username,instance.user.id,filename)

class MyUserManager(UserManager):
    def create_user(self, username, email, password,superuser=False,staff=False,**kwargs):
        if not email or not password:
            raise ValueError('Users must have an email and a password')
        user_obj = self.model(email=self.normalize_email(email))
        user_obj.username = username
        user_obj.set_password(password)
        user_obj.is_active = True
        user_obj.is_superuser = superuser
        user_obj.is_staff = staff
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self,username, email, password,**kwargs):
        user = self.create_user(username, email,password, superuser=True,staff=True,**kwargs)
        return user

class MyUser(AbstractUser):
    email           = models.EmailField(unique=True, blank=False, null=False)
    objects         = MyUserManager()

def user_post_save_receiver(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
post_save.connect(user_post_save_receiver, MyUser)

class Profile(models.Model):
    user            = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete = models.CASCADE, blank=True, null=True)
    username        = models.SlugField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to = uploadedfile_path, default='profiles/default/index.png')
    status          = models.TextField(default='hey there im using MyChatApp!')
    created         = models.DateTimeField(auto_now = True)

    class Meta:
        permissions = [
            ('change_Profile','Can change ProfileModel'),
            ('view_Profile','Can view ProfileModel'),
            ('delete_Profile','Can delete ProfileModel'),
            ('add_Profile','Can add ProfileModel'),
        ]

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile-detail', args=[self.username])

def pre_save_receiver(sender, instance, **kwargs):
    instance.username = slugify(instance.user.username)
pre_save.connect(pre_save_receiver, Profile)

def post_save_receiver(sender, instance, created, **kwargs):
    if created:
        perms = ['chat.change_Profile','chat.delete_Profile','chat.view_Profile','chat.add_Profile']
        for perm in perms:
            assign_perm(perm, instance.user, instance)
post_save.connect(post_save_receiver, Profile)

class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank=True, null=True)
    text = models.CharField(max_length = 255)
    created = models.DateTimeField(auto_now = True)
    receiver = models.CharField(max_length = 255)
    
    def __str__(self):
        return self.text
