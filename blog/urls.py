from django.conf.urls import url
from blog import views


urlpatterns = [
    url(r'^$', views.PostListView.as_view(), name='post_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',
        views.post_detail, name='post_detail'),
    url(r'^(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),
    url(r'^login/$', views.user_login, name='login'),
    #url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    #url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    #url(r'^logout-then-login/$', 'django.contrib.auth.views.logout_then_login', name='logout_then_login'),
    #url(r'^$', views.dashboard, name='dashboard'),
]
