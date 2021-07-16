from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,authenticate,login
from testApp.forms import SignUpForm
from django.http import HttpResponseRedirect

# Create your views here.

def home_page(request):
    return render(request, 'testApp/home.html')


@login_required   # login_url optional parameter
def Java_exam(request):
    return render(request, 'testApp/javaexam.html')


@login_required
def python_exam(request):
    return render(request, 'testApp/pythonexam.html')


def aptitude_exam(request):
    return render(request, 'testApp/aptitudeExam.html')

def sinUp_view(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            return HttpResponseRedirect('/accounts/login')
    return render(request,'testApp/signup.html',{'form':form})

#def login_view(request):
#    username = request.POST['username']
#    password = request.POST['password']
#    msg =''
#    user = authenticate(request, username=username, password=password)
#    if user is not None:
#        login(request, user)
#        msg = "sucessfully"
#    else:
#        msg = "Invalid"

#    return render(request, 'testApp/login_success.html',{'msg':msg})

#def logout_view(request):
#    logout(request)
#    return render(request, 'testApp/logout.html')