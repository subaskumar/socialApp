from django.shortcuts import render
from moviesApp.forms import moviesAdd
from moviesApp.models import movieUpcoming
# Create your views here.

def home_page(request):
    
    return render(request, 'moviesApp/index.html')

def movies_form(request):

    form = moviesAdd()
    if request.method == 'POST':
        form = moviesAdd(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return home_page(request)
    return render(request,'moviesApp/addMovie.html',{'form':form} )

def list_movies(request):
    movie_list = movieUpcoming.objects.order_by('rdate')

    return render(request,'moviesApp/listMovie.html',{'movie_list':movie_list} )