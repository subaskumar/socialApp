from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from decimal import *

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, phone,name,email, password=None, is_staff=False, is_active=True, is_admin=False):
        if not phone:
            raise ValueError('users must have a phone number')

        if not password:
            raise ValueError('user must have a password')

        user_obj = self.model(phone=phone)
        user_obj.name = name
        user_obj.email = email
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone,name=None,email=None, password=None):
        user = self.create_user(phone,name,email, password=password,is_staff=True,)
        return user

    def create_superuser(self, phone,name=None,email=None,password=None):
        user = self.create_user(phone,name=name,email=email, password=password,is_staff=True,is_admin=True,)
        return user


class User(AbstractBaseUser):
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone       = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    name        = models.CharField(max_length = 20, blank = True, null = True)
    email       = models.EmailField(max_length=254,blank = True, null = True)
    first_login = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)
    timestamp   = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.phone)

    def get_full_name(self):
        return self.phone

    def get_short_name(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):

        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
    

def upload_profile_to(instance,filename):
	return f'profile_picture/{instance.user.phone}/{filename}'

def upload_cover_to(instance,filename):
	return f'coverImage/{instance.user.phone}/{filename}'
 
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
class Profile(models.Model):
    gen = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    about_me = models.CharField(max_length=250, null=True)
    birthday = models.DateField(null=True)
    profile_pic = models.ImageField(upload_to = upload_profile_to, null=True, default = 'defaults/profile_pic.jpg')
    cover_image = models.ImageField(upload_to = upload_cover_to, null = True, default= 'defaults/cover_image.jpg')
    gender = models.CharField(choices=gen, max_length=6, null=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    following = models.ManyToManyField(User, related_name="following", blank=True)
    def __str__(self):
        return self.user.phone
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_pic.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)
        img2 = Image.open(self.cover_image.path)
        if img2.height > 500 or img2.width > 500:
            output_size = (500, 500)
            img2.thumbnail(output_size)
            img2.save(self.cover_image.path)
    def non_followed_user(self):
        return set(User.objects.filter(active=True))-set(self.following.all())-{self.user}
    def get_notifications(self):
        return Notification.objects.filter(user=self.user, seen = False)
    @receiver(post_save, sender=User)
    def update_profile_signal(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

        
class Notification(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	message = models.CharField(max_length=500)
	link = models.CharField(max_length=500)
	seen = models.BooleanField(default=False)
 

def upload_post_to(instance,filename):
	return f'post_picture/{instance.user.phone}/{filename}'

class Post(models.Model):
    PRIVACY_CHOICES = (('Public', 'Public'), ('Friends', 'Friends'), ('Onlyme', 'Onlyme'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    picture = models.ImageField(null=True, upload_to = upload_post_to,)
    privacy = models.CharField(max_length=9, choices=PRIVACY_CHOICES, default='Public')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name='likes')
    dislikes = models.ManyToManyField(User,related_name='dislikes')
    class Meta:
        ordering = ('-created_at',)

class Like(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)

class Dislike(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)	

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)
	comm = models.TextField()

class SubComment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)
	comm = models.TextField()
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE)