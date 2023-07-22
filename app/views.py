from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Ihas
from .forms import IhasForm
from baykar import settings 
from django.db.models import Q
import chunk
import os
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    data_list = Ihas.objects.all()
    return render(request, 'home.html', {'data_list': data_list})
def search_view(request):
    data_list = Ihas.objects.all()
    query = request.GET.get('q', '')  # Boş bir değer atama
    print(query)
    if query:
      results = Ihas.objects.filter(adi__icontains=query)
    else:
        results = data_list

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'home.html', context)
#iha silme
def delete_iha(request, id):
    iha = Ihas.objects.get(id=id)  # İha nesnesini doğru şekilde alın
    print(iha)
    if request.method == 'POST':
        # İha'yı silme işlemini gerçekleştirin
        iha.delete()
        return redirect('show_all')  # Silme işleminden sonra yönlendirilecek sayfa

    context = {'iha': iha}
    return render(request, 'delete.html', context)
def duzenle_iha(request, id):
    iha = Ihas.objects.get(id=id)
    if request.method == 'POST':
        ihname = request.POST.get('ihaisim')
        ihyıl = request.POST.get('yıl')
        ihrenk = request.POST.get('renk')
        ihozellik = request.POST.get('ozellik')
        form = request.FILES.get('file')
        if form is not None:
            print(form)
            ihyol = form.name
            file_path = os.path.join('static/img', form.name)
            with open(file_path, 'wb') as f:
                for chunk in form.chunks():
                    f.write(chunk)
            
            print(ihname, ihyıl, ihrenk, ihozellik, ihyol)
            ihas = Ihas(adi=ihname, renk=ihrenk, ozellikler=ihozellik, yıl=ihyıl,dosya_yolu=ihyol)
            ihas.save()
    context = {'iha': iha}
    return render(request, 'duzenle.html', context)
def duzenle_iha(request, id):
    iha = Ihas.objects.get(id=id)
    print(iha.ozellikler)
    if request.method == 'POST':
        ihname = request.POST.get('ihaisim')
        ihyıl = request.POST.get('yıl')
        ihrenk = request.POST.get('renk')
        ihozellik = request.POST.get('ozellik')
        form = request.FILES.get('file')
        if form is not None:
            print(form)
            ihyol = form.name
            file_path = os.path.join('static/img', form.name)
            with open(file_path, 'wb') as f:
                for chunk in form.chunks():
                    f.write(chunk)
            # Mevcut iha nesnesini güncelle
        iha.adi = ihname
        iha.yıl = ihyıl
        iha.renk = ihrenk
        iha.ozellikler = ihozellik
        iha.dosya_yolu = form.name
        iha.save()
        return render(request, 'home.html')
    context = {'iha': iha}
    return render(request, 'duzenle.html', context)
@login_required
def filter_results(request):
    if request.method == 'GET':
        renk = request.GET.get('renk')
        yıl = request.GET.get('yil')
        kelime=request.GET.get('kelime')
        
        if renk and yıl:
            results = Ihas.objects.filter(renk=renk, yıl__lt=yıl)
        elif renk:
            results = Ihas.objects.filter(renk=renk)
        elif yıl:
            results = Ihas.objects.filter(yıl__lt=yıl)
        else:
            results = Ihas.objects.all()
        if kelime:
            results = results.filter(Q(ozellikler__icontains=kelime) | Q(adi__icontains=kelime))
        context = {
            'results': results
        }
        return render(request, 'home.html', context)
#filtrelemeden ayrı uygulamanın herhangi bir yerinde bütün verilere ihtiyac halinde kullanılacak blok
    
@login_required
def  show_all(request):
     results = Ihas.objects.all()
     return render(request, 'home.html', results)
def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')


        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:
            selam=make_password(pass1)
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.first_name=selam
            my_user.save()

            return redirect('login')
        



    return render (request,'signup.html')
#Giriş sayfası bloğu kullanıcı bilgileri kontrol eder

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            datalist=Ihas.objects.all();
            return render(request,'home.html',{'datalist':datalist})
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')
#Kullanıcı çıkış bloğu

def LogoutPage(request):
    logout(request)
    return redirect('login')
#İhaların alındığı ve veritabanına kayıt edildiği blok
@login_required   
def ekleme(request):
      if request.method == 'POST':
        ihname = request.POST.get('ihaisim')
        ihyıl = request.POST.get('yıl')
        ihrenk = request.POST.get('renk')
        ihozellik = request.POST.get('ozellik')
        form = request.FILES.get('file')
        if form is not None:
            print(form)
            ihyol = form.name
            file_path = os.path.join('static/img', form.name)
            with open(file_path, 'wb') as f:
                for chunk in form.chunks():
                    f.write(chunk)
            
            print(ihname, ihyıl, ihrenk, ihozellik, ihyol)
            ihas = Ihas(adi=ihname, yıl=ihyıl, renk=ihrenk, ozellikler=ihozellik, dosya_yolu=ihyol)
            ihas.save()
            return redirect('ekle')

      return render(request, 'ekle.html')
