# templatetags/filter.py
# navbar에서 client 로그인 한 사람과 partner 로그인 한 사람 구별해서 화면 제어
from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, client):
    # group = Group.objects.get(name=client)
    return True if user.groups.filter(name=client).exists() else False
