from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',    
    url(r'^add/$', add, name="add"),
    url(r'^read/$', read, name="read"),
    url(r'^messages/$', messages, name="messages"),
    url(r'replace_captcha/$',replace_captcha,name='replace-captcha'),
)
