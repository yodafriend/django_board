from django.shortcuts import redirect, render
from .models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def index(request):
    return render(request,"acc/index.html")

def signup(request):
    if request.method=="POST":
        un = request.POST.get("username")
        pw = request.POST.get("password")
        ni = request.POST.get("nickname")
        co = request.POST.get("comment")
        pi = request.FILES.get("pic")
        User.objects.create_user(username=un,password=pw,nickname=ni,comment=co,pic=pi)
        return redirect("acc:login")
    return render(request,"acc/signup.html")

def userlogin(request):
    if request.method=="POST":
        un = request.POST.get("username")
        pw = request.POST.get("password")
        user=authenticate(username=un,password=pw)
        if user:
            login(request,user)
        return redirect("acc:index")
    return render(request,"acc/login.html")

def userlogout(request):
    logout(request)
    return redirect("acc:index")

def profile(request):
    return render(request,"acc/profile.html")

def update(request):
    if request.method=="POST":
        user=request.user
        pw = request.POST.get("password")
        ni = request.POST.get("nickname")
        co = request.POST.get("comment")
        pi = request.FILES.get("pic")
        if pw:
            user.set_password(pw)
        user.nickname=ni
        user.comment=co
        if pi:
            user.pic.delete()
            user.pic =pi
        user.save()
        login(request,user)
        return redirect("acc:profile")
    return render(request,"acc/update.html")

def remove(request):
    request.user.delete()
    return redirect("acc:login")