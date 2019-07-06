from django.contrib.auth import (
    authenticate,
    login as auth_login,
)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from partner.models import Partner,Menu
from client.models import Order, OrderItem


# Create your views here.
def index(request):
    partner_list = Partner.objects.all()
    ctx = {
        "partner_list" :partner_list
    }
    return render(request, "main.html", ctx)


def common_login(request, ctx, group):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password) #from에 import한 함수를 가져다 써줌
        if user is not None:
# group은 class, user가 가진 전체 group 중 group의 이름만 꺼내는 list 만듦
            if group not in [group.name for group in user.groups.all()]:
                ctx.update({"error":"접근 권한이 없습니다."})
                for group in user.groups.all():
                    print("group:",group)

            else:
                auth_login(request, user)
                next_value = request.GET.get("next") #next로 깃발 꽂기
                if next_value:
                    return redirect(next_value)
                else: # client 로그인 했는데 메뉴 추가 나오는 문제 해결
                    if group == "partner": # partner로 들어오는 경우
                        return redirect("/partner/")
                    else: # clinet로 들어오는 경우
                        return redirect("/")

        else:
            ctx.update({"error":"사용자가 없습니다."})

    return render(request, "login.html",ctx)

# login
def login(request):
    ctx = {"is_client":True}
    return common_login(request, ctx,"client")


def common_signup(request, ctx, group):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.create_user(username, email, password)
        target_group = Group.objects.get(name=group)
        user.groups.add(target_group)
        # print(username, email, password)

        if group == "client": # partner와 달리 client는 추가 정보 입력 안받음
            Client.objects.create(user=user, name=username)
    return render(request, "signup.html",ctx)

#signup
def signup(request):
    ctx = {"is_client":True}
    return common_signup(request, ctx,"client")

def order(request, partner_id):
    ctx = {}
    # if request.user.is_anonymous or request.user.partner is None:
    #     return redirect("/partner/")
    partner = Partner.objects.get(id=partner_id)
    menu_list = Menu.objects.filter(partner=partner)

    if request.method == "GET":
        ctx.update({
            "partner": partner,
            "menu_list": menu_list,
        })
    elif request.method == "POST":
        # menu_dict = {}
        order = Order.objects.create(
            client=request.user.client,
            address="test",
        )
        for menu in menu_list:
            menu_count = request.POST.get(str(menu.id)) #order_menu_list에 수량 input에 있는 menu.id 가져옴
            # if int(menu_count) > 0:
            #     menu_dict.update({ str(menu.id): menu_count })
            menu_count = int(menu_count) #모든 post 방식은 text로 받으니 int 변환 필요
            if menu_count > 0:
                item = OrderItem.objects.create( #model 가서 orderitem 보기
                    order=order,
                    menu=menu,
                    count=menu_count
                )
                # order.items.add(item) 이미 위에서 create 했으니 add할 필요 없음

        return redirect("/")

    return render(request, "order_menu_list.html", ctx)
