from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
import sys

def debug_print(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()
@csrf_protect
def index(request):
    return render(request,"index.html")
# Create your views here.
@csrf_protect
def HomePage(request):
    return render (request,'home.html')
@csrf_protect
def SignupPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if(pass1!=pass2):
            my_user=User.objects.create_user(username,email,pass1)
            my_user.save
            debug_print(username,email,pass1,pass2)
            return HttpResponse("Başarılı bir şekilde oluşturuldu")
        else:
            return HttpResponse("Başarısız")

            pass
    
    return render(request, 'signup.html')

def  LoginPage(request):
    return render(request,'login.html')
