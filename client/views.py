from django.shortcuts import render
from partner.models import Partner #Partner 폴더의 모델 가져와서 씀

# Create your views here.
def index(request):
    partner_list = Partner.objects.all()
    ctx = {
        "partner_list" :partner_list
    }
    return render(request, "main.html", ctx)
