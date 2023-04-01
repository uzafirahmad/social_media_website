import imp
from pyexpat import model
from sqlite3 import Timestamp
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date
from django.conf import settings
import string
import random
from datetime import datetime
from .validators import file_size,image_size

def __str__(self):
    return self.username

def has_perm(self,perm,obj=None):
    return self.is_admin

def has_module_perms(self,app_label):
    return True

def id_generator(size=50, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_profle_image_filepath(instance,filename):
    return f'profile_images/{instance.email}/{"profile_image.png"}'

def get_post_image_filepath(instance,todaysdate):
    return f'posts/{instance.post_owner.subsection_owner.section_owner.email}/{date.today()}/{"postpicture.png"}'

def get_post_video_filepath(instance,todaysdate):
    return f'posts/{instance.post_owner.subsection_owner.section_owner.email}/{date.today()}/{"postvideo.mp4"}'

def get_notification_image_filepath(instance,filename):
    return f'notifications/{instance.notification_owner.email}/{"notification_image.png"}'

# Create your models here.
class MyUserManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("users must have a username")
        user= self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class Accounts(AbstractBaseUser, PermissionsMixin):
    email=models.EmailField(verbose_name="email",max_length=60,unique=True)
    stripe_customer_id=models.CharField(max_length=1000,blank=True,null=True)
    username=models.CharField(max_length=30, unique=True)
    followers=models.IntegerField(default=0)
    following=models.IntegerField(default=0)
    follow_fee=models.IntegerField(default=15,validators=[MinValueValidator(1)])
    earnings=models.IntegerField(default=0)
    timezone=models.CharField(default="GMT+01:00",max_length=100)
    biodescription=models.CharField(max_length=4000, default="Hey there!", blank=True)
    date_joined=models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    last_login=models.DateTimeField(verbose_name="last login",auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    profile_image=models.ImageField(max_length=255, upload_to=get_profle_image_filepath, null=True, blank=True, default="default/default.png",validators=[image_size])
    password=models.CharField(max_length=100)
    description=models.CharField(max_length=10000, default="", blank=True)
    auth_token=models.CharField(max_length=100, default="")
    password_auth=models.CharField(max_length=100, default="",unique=True, editable = False)
    ban=models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS = ['username']

class sections(models.Model):
    section_name=models.CharField(default="",max_length=30)
    viewable_to=models.CharField(default="Everyone",max_length=15)
    sec_description=models.CharField(default="",max_length=10000, blank=True,verbose_name="Section Description:")
    section_owner = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    def __str__(self):
        return self.section_name

class subsections(models.Model):
    subsection_serial=models.IntegerField(default=0)
    subsection_add_date=models.CharField(verbose_name="Date added",default="",blank=True,max_length=100)
    subsection_owner = models.ForeignKey(sections, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.subsection_serial)

class posts(models.Model):
    post_hash=models.CharField(default="",max_length=10000, editable = False)
    post_time=models.CharField(default="",max_length=1000)
    post_text=models.CharField(default="",max_length=100000,blank=True)
    post_image=models.ImageField(max_length=100000, upload_to=get_post_image_filepath, null=True, blank=True,validators=[image_size])
    post_video=models.FileField(upload_to=get_post_video_filepath, null=True, blank=True,validators=[file_size])
    post_owner=models.ForeignKey(subsections, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.post_time)

class followerslist(models.Model):
    fuser=models.ForeignKey(Accounts,on_delete=models.CASCADE)
    email=models.CharField(default="",max_length=10000)
    subscription_id=models.CharField(default="",max_length=100,null=True,blank=True)
    def __str__(self)->str:
        return self.email

class followinglist(models.Model):
    fuser=models.ForeignKey(Accounts,on_delete=models.CASCADE)
    email=models.CharField(default="",max_length=10000)
    subscription_id=models.CharField(default="",max_length=100,null=True,blank=True)
    def __str__(self)->str:
        return self.email

class ChatFather(models.Model):
    thread_name=models.CharField(null=True,blank=True,max_length=50)

    def __str__(self)->str:
        return self.thread_name

class ChatModel(models.Model):
    sender=models.CharField(max_length=100,default=None)
    message=models.TextField(null=True,blank=True)
    thread_owner=models.ForeignKey(ChatFather, on_delete=models.CASCADE)
    message_id=models.CharField(default=id_generator(),max_length=10000)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self)->str:
        return self.sender

class notifications(models.Model):
    notification_choices = (
        ("follow_key", "follow"),
        ("posted_key", "posted"),
        ("message_key", "message"),
        ("website_key", "website"),
    )
    notification_id=models.CharField(default=id_generator(),max_length=10000)
    notification_read=models.BooleanField(default=False)
    notification_type=models.CharField(max_length=100, choices=notification_choices, default="website_key")
    notification_text=models.CharField(max_length=1000,blank=True,null=True)
    notification_image=models.ImageField(max_length=255, upload_to=get_notification_image_filepath, null=True, blank=True, default="default/defaultnotifications.png")
    notification_date=models.CharField(default=datetime.now().strftime("%B %d, %Y"),max_length=1000)
    notification_owner=models.ForeignKey(Accounts, on_delete=models.CASCADE)
    notification_username_case=models.CharField(max_length=1000,blank=True,null=True,default="x")
    notification_sectionname_case=models.CharField(max_length=1000,blank=True,null=True,default="x")

    def __str__(self)->str:
        return self.notification_text