from django.conf.urls import url
from comment.views import comment_create

app_name = 'comment'


urlpatterns = [
    # url(r'^create/$', comment_create, name='comment_create'),
    url(r'^create/(?P<id>[0-9]+)/$', comment_create, name='create'),
    ]

