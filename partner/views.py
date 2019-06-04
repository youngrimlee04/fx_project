from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import PartnerForm


# Create your views here.
def index(request): #ctx에 담아서 form 넘김
    ctx = {}
    if request.method=="GET":
        partner_form=PartnerForm()
        ctx.update({"form" : partner_form})
    elif request.method=="POST":
        partner_form=PartnerForm(request.POST)
        if partner_form.is_valid():
            partner=partner_form.save(commit=False) # save의 commit은 db에 저장할지 묻는것
            partner.user=request.user # user 집어넣기
            partner.save()
            return redirect("/partner/")
# 저장 안하는 이유는? model에서는 user있는데 form에서 없기 때문에
        else:
            ctx.update({"form" : partner_form})

    return render(request, "index.html",ctx)

def login(request):
    ctx = {}

    if request.method == "GET":
        pass
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("/partner/")
        else:
            ctx.update({"error":"사용자가 없습니다."})

    return render(request, "login.html",ctx)

def signup(request):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.create_user(username, email, password)

    ctx={}
    return render(request, "signup.html",ctx)

def logout(request):
    auth_logout(request)
    return redirect("/partner/")

def edit_info(request):
    ctx = {}
    # Article.objects.all() 같은 쿼리(DB에 질문 통해 data 가져옴)
    if request.method=="GET":
        partner_form=PartnerForm(instance=request.user.partner)
        ctx.update({"form" : partner_form})
    elif request.method=="POST":
        partner_form=PartnerForm(
            request.POST,
            instance=request.user.partner
        )
        if partner_form.is_valid():
            partner = partner_form.save(commit=False) # save의 commit은 db에 저장할지 묻는것
            partner.user=request.user
            partner.save()
            return redirect("/partner/")
# 저장 안하는 이유는? model에서는 user있는데 form에서 없기 때문에 user 집어넣어야 해서
        else:
            ctx.update({"form" : partner_form})

    return render(request, "edit_info.html",ctx)    
