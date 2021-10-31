"""SocialProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name = 'login'),
    path('logout/', logout_view, name = 'logout'),
    path('signup/', signup, name = 'signup'),
    path('search/', search, name = 'search'),
    path('profile/<int:id>', profile, name = 'profile'),
    path('', home, name = 'home'),
    path('followers/<int:id>/', followers, name = 'follower'),
	path('following/<int:id>/', following, name = 'following'),
	path('mutualFriends/<int:id>/', mutualFriends, name = 'mutual'),
    path('follow/', follow , name = 'follow'),
    path('unfollow/', unfollow, name = 'unfollow'),
]

if settings.DEBUG:
	urlpatterns+= static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
	urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)