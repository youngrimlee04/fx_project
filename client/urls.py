from django.conf.urls import url, include
from .views import (
    index,
)

urlpatterns = [
    url(r'^$',index, name="index"),
    # url(r'^signup/$', signup,name="signup"),
    # url(r'^login/$', login,name="login"),

]
