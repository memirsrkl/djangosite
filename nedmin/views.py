from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from .models import admins
from .models import yazilar
from .forms import adminslogin
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import validate_email
def sanitize_email(email):
    try:
        email = validate_email(email)
        return email
    except ValidationError:
        return None
control=True
def AdminGiris(request):
    return render(request, 'admintemp/login.html')
def AdminLogin(request):
 if control:
    if request.method == 'POST':
        admin_name = request.POST.get('adminname')
        admin_pass = request.POST.get('adminpass')
        try:
            admin_user = admins.objects.get(admin_name=admin_name, admin_pass=admin_pass)
        except ObjectDoesNotExist:
            return render(request, 'admintemp/login.html')
        if admin_user is not None:
            user = authenticate(request, username=admin_name, password=admin_pass)
            if user is not None:
                login(request, user)
                return redirect('admin_homepage', admin_user.id)
            else:
                messages.error(request, 'Geçersiz kullanıcı adı veya parola')
                return redirect('admin_login')
        else:
            error_message = 'Geçersiz kullanıcı adı veya parola'
            return HttpResponse("selam")
    else:
        print("selam")
        return render(request, 'admintemp/login.html')
@login_required(login_url='admin_login')
def AdminHomePage(request, id):
    try:
        adm = admins.objects.get(id=id)
    except admins.DoesNotExist:
        return HttpResponse('Geçersiz kullanıcı')
    context = {'adm': adm}
    return render(request, 'admintemp/adminhomepage.html', context)
def sifreyenile(request):
    if request.method=='POST':
        admin_name = request.POST.get('adminname')
        admin_email = request.POST.get('admineposta')
        admin_token=request.POST.get('token')
        try:
            admin_user=admins.objects.get(admin_name=admin_name,admin_email=admin_email)
        except ObjectDoesNotExist:
            return HttpResponse("Kullanıcı Adı veya Eposta yanlış")
        if(admin_token=='pbkdf2_sha256$260000$IeeYizkQNGw5VoGZnuBVoo$8OZOa6B5ucYF6MJ9K1cifrz63yY4I0m8aqI7zdYqrHA='):
            print(admin_user)
            context = {
                'admin_user' : admin_user,
            }
            return render(request,"paschangesucces.html",context)
        else:
            return HttpResponse("Token Yanlış")
    return render(request,'sifreyenile.html')
def AdminLogout(request):
    logout(request)
    control=False
    return redirect('admin_login')
def Edit(request):
    adm=admins.objects.all()
    context = {
        'adm':adm,
    }
    return redirect(request,'admintemp/adminhomepage.html',context)
def asilsifreyenile(request,id):
    if request.method=="POST":
        user=admins.objects.get(id=id)
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        token="pbkdf2_sha256$260000$IeeYizkQNGw5VoGZnuBVoo$8OZOa6B5ucYF6MJ9K1cifrz63yY4I0m8aqI7zdYqrHA="
        context = {
                    'user_name': user.admin_name,
                    'new_password': pass1,
                    'token': token,
                }
        html_message = render_to_string('email.html', context)
        if(pass1==pass2):
            plain_message = strip_tags(html_message)
            send_mail(
                'Şifre yenileme',
                'Şifreniz yenilendi Token adresiniz pbkdf2_sha256$260000$IeeYizkQNGw5VoGZnuBVoo$8OZOa6B5ucYF6MJ9K1cifrz63yY4I0m8aqI7zdYqrHA= ',
                 user.admin_email,  # Gönderen e-posta adresi
                [user.admin_email, 'emirsrkl@hotmail.com'],  # Alıcı e-posta adresi veya adresleri (liste olarak)
                fail_silently=True,  # E-posta gönderimi başarısız olduğunda hata gösterilsin mi?
                html_message=html_message,)
            user2=User.objects.get(username=user.admin_name,email=user.admin_email)
            user2.password=make_password(pass1)
            user.admin_pass=pass1
            user2.save()
            user.save()
            return HttpResponse("helal")
    return redirect("asilsifreyenile")
def update(request,id):
    if request.method == 'POST':
        adm = admins.objects.get(id=id)
        admin_name = request.POST.get("admin_name")
        admin_pass = request.POST.get("admin_pass")
        admin_realname = request.POST.get("admin_realname")
        admin_surname = request.POST.get("admin_surname")
        admin_insta = request.POST.get("admin_insta")
        admin_twitter = request.POST.get("admin_twitter")
        admin_email = request.POST.get("admin_email")
        admin_phone = request.POST.get("admin_phone")
        admin_adress = request.POST.get("admin_adress")
        user = User.objects.get(username=adm.admin_name)
        if check_password(adm.admin_pass,user.password):
            user.username=admin_name
            user.password=make_password(admin_pass)
            user.save()
        else:
            return HttpResponse("Kullanıcı Eşleşmedi")
        adm.admin_name = admin_name
        adm.admin_pass = admin_pass 
        adm.admin_realname = admin_realname
        adm.admin_surname = admin_surname
        adm.admin_insta = admin_insta
        adm.admin_twitter = admin_twitter
        adm.admin_email = admin_email
        adm.admin_phone = admin_phone
        adm.admin_adress = admin_adress
        adm.save()
        return redirect('admin_homepage',id=id)
    return render(request,'admintemp/adminhomepage.html')
def user_info_view(request,id):
    adm=admins.objects.get(id=id)
    context = {
        'adm' : adm
    }
    return render(request, 'user_info.html',context)

def contact_view(request):
    yaz = yazilar.objects.all()
    return render(request, 'contact.html',{'yaz':yaz})

def add_post_view(request):
    # Yazı Ekle ile ilgili işlemleri burada yapın
    return render(request, 'add_post.html')

def new_page_view(request):
    # Yeni Sayfa ile ilgili işlemleri burada yapın
    return render(request, 'new_page.html')
def yazisil(request,id):
    print(id)
    yaz=yazilar.objects.all()
    return render(request, 'admintemp/adminhomepage.html',id=id)