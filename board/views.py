from django.shortcuts import render,redirect
from django.utils import timezone
from .models import Board,Reply
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    
    b= Board.objects.all()
    page=request.GET.get("page",1)
    cate=request.GET.get("cate","")
    kw = request.GET.get("kw","")
    if kw:
        if cate=="sub":
            b=Board.objects.filter(subject__startswith=kw)
        elif cate=="wri":
            b=Board.objects.filter(writer=kw)
        elif cate=="con":
            b=Board.objects.filter(content__contains=kw)
        else:
            b= Board.objects.all()
    else:
        b= Board.objects.all()
    b=b.order_by("-pubdate")
    pag = Paginator(b,10)
    obj=pag.get_page(page)

    context={
        "blist":obj,
        "cate":cate,
        "kw":kw,
    }
    return render(request,"board/index.html",context)

def create(request):
    if request.method == "POST":
        su = request.POST.get("subject")
        if su:
            wr = request.user.username
            co = request.POST.get("content")
            Board(subject=su, writer=wr, content=co, pubdate=timezone.now()).save()
            return redirect("board:index")
        else:
            messages.error(request, "제목을 넣어주세요")
    return render(request, "board/create.html")

def detail(request,bpk):
    b=Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context={
        "bo":b,
        "re":r,
    }
    return render(request,"board/detail.html",context)

def update(request,bpk):
    b=Board.objects.get(id=bpk)
    if request.user.username != b.writer:
        return render(request,"error/forbidden.html")
    if request.method=="POST":
        sub=request.POST.get("subject")
        con = request.POST.get("content")
        b.subject=sub
        b.content=con
        b.save()
        return redirect("board:detail",bpk=bpk)
    context={
        "bo":b
    }
    return render(request,"board/update.html",context)
def delete(request,bpk):
    b=Board.objects.get(id=bpk)
    if request.user.username != b.writer:
        return render(request,"error/forbidden.html")
    b.delete()
    return redirect("board:index")

def create_reply(request,bpk):
    com=request.POST.get("comment")
    if com:
        b=Board.objects.get(id=bpk)
        rep=request.user.username
        Reply(sub=b,replyer=rep,comment=com).save()
    return redirect("board:detail",bpk=bpk)
def remove_reply(request,bpk,rpk):
    r= Reply.objects.get(id=rpk)
    if r.replyer != request.user.username:
        return render(request,"error/forbidden.html")
    r.delete()
    return redirect("board:detail",bpk=bpk)

def likey(request,bpk):
    b=Board.objects.get(id=bpk)
    b.likey.add(request.user)
    return redirect("board:detail",bpk=bpk)
def unlikey(request,bpk):
    b=Board.objects.get(id=bpk)
    b.likey.remove(request.user)
    return redirect("board:detail",bpk=bpk)