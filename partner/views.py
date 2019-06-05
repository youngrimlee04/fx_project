from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import PartnerForm, MenuForm
from .models import Menu


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
    if request.method =="GET":
        partner_form=PartnerForm(instance=request.user.partner)
        ctx.update({"form" : partner_form})
    elif request.method =="POST":
        partner_form=PartnerForm(
            request.POST, # Create a form to edit an existing info, but use POST data to populate the form.
            instance=request.user.partner
        )
        if partner_form.is_valid():
            partner = partner_form.save(commit=False)
            partner.user=request.user
            partner.save()
            return redirect("/partner/")

        else:
            ctx.update({"form" : partner_form})

    return render(request, "edit_info.html",ctx)

def menu(request): # Declare the ForeignKey with related_query_name
    ctx={}

    menu_list = Menu.objects.filter(partner = request.user.partner)
    ctx.update({"menu_list":menu_list})
    return render(request, "menu_list.html",ctx)

def menu_add(request):
    ctx={}
    # if "partner" not in request.user.groups.all(): #request,user,group 안의 모든 것 가져옴
    #     return redirect(URL_LOGIN)

    if request.method=="GET":
        form=MenuForm()
        ctx.update({"form":form})
    elif request.method=="POST":
        form=MenuForm(request.POST, request.FILES) #위와 다르게 파일 함께 저장한다는 의미로 request.FILES
        if form.is_valid():
            menu = form.save(commit=False) #메뉴 인스턴스 생성
            menu.partner = request.user.partner
            menu.save()
            return redirect("/partner/menu/")
        else: #에러시 저장 안하고 에러표시와 함께 처리
            ctx.update({"form":form})

    return render(request, "menu_add.html",ctx)
