from django.shortcuts import render, redirect,get_object_or_404
from .forms import SignUpForm,UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
import random
from .models import Profile, Notification,Post, Like, Dislike, Comment, SubComment
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
#from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()

#from socialApp.models import Post

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'user/signup.html', {'form':form})
    else:
        form = SignUpForm()
        return render(request, 'user/signup.html', {'form':form})



def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        phone = request.POST['phone']
        password = request.POST['password']
        user = authenticate(request,phone=phone, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'user/login.html', {'form': form,})

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def home(request):
    if request.method == "POST":
        text = request.POST.get('text')
        img = request.FILES.get('post_image')
        privacy = request.POST.get('privacy')
        post = Post(user = request.user, text = text, picture=img, privacy = privacy)
        post.save()
        mess = f"{request.user.name} added a Post."
        for usr in request.user.profile.followers.all():
            noti = Notification(user = usr, message=mess, link = f"/#post{post.id}")
            noti.save()
        return redirect('home')
    following_users = list(request.user.profile.following.all())
    following_users.append(request.user)
    posts = Post.objects.filter(user__in = following_users).order_by('-created_at')
    parms = {
		'non_followed_user': request.user.profile.non_followed_user,
		'posts': posts,
	}
    return render(request, 'user/home.html', parms)

# User Profile View
@login_required
def profile(request, id):
    user = User.objects.filter(id=id)
    if request.user == user.first():
        parms = {
			'useritself': True,
			'user': request.user
			}
    else:
        their_followers = user.first().profile.followers.all()
        my_follwoing = request.user.profile.following.all()
        intersection = their_followers & my_follwoing
        print(intersection)
        parms = {
			'useritself': False,
			'user': user.first(),
			'mutual': intersection
		}
    posts = Post.objects.filter(user = user.first()).order_by('-created_at')
    parms['posts'] = posts
    return render(request, 'user/profile.html', parms)

@login_required
def search(request):
    if 'term' in request.GET:
        qs = request.GET.get('term')
        users = User.objects.filter(Q(phone__istartswith = qs) |Q(name__istartswith = qs) |Q(email__istartswith = qs))
        user_list = list()
        for usr in users:
            user_list.append(usr.name)
        return JsonResponse(user_list, safe=False)
        
    if request.method == 'POST':
        q = request.POST.get('q')
        if q:
            users = User.objects.filter(Q(phone__icontains = q) |Q(name__icontains = q) |Q(email__icontains = q))
        else:
            users = request.user.profile.non_followed_user
            
        return render(request, 'user/search.html', {'users': users})
    return render(request, 'user/search.html')


@login_required
@csrf_exempt
def follow(request):
    if request.method == "POST":
        usrname = request.POST.get('user')
        following = get_object_or_404(User, phone = usrname)
        following.profile.followers.add(request.user)
        request.user.profile.following.add(following)
        mess = f"{request.user.name} started following you."
        noti = Notification(user = following, message=mess, link = f"/user/{request.user.phone}")
        noti.save()
        return HttpResponse(True)
    raise Http404()

@login_required
@csrf_exempt
def unfollow(request):
	if request.method == "POST":
		usrname = request.POST.get('user')
		following = get_object_or_404(User, phone = usrname)
		following.profile.followers.remove(request.user)
		request.user.profile.following.remove(following)
		return HttpResponse(True)
	raise Http404()

@login_required
def following(request,id):
    user = User.objects.get(id = id)
    following = user.profile.following.all()
    return render(request, 'user/search.html', {'users': following}) 	

@login_required
def followers(request,id):
    user = User.objects.get(id = id)
    followers = user.profile.followers.all()
    return render(request, 'user/search.html', {'users': followers})

@login_required
def mutualFriends(request,id):
    user = User.objects.filter(id=id)
    their_followers = user.first().profile.followers.all()
    my_follwoing = request.user.profile.following.all()
    intersection = their_followers & my_follwoing
    return render(request, 'user/search.html', {'users': intersection})