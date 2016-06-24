from django.conf.urls import url, include
from blog import views
from django.contrib.auth.views import login, password_change, password_change_done, \
                                      password_reset, password_reset_done, \
                                      password_reset_confirm, password_reset_complete


urlpatterns = [
    url(r'^$', views.PostListView.as_view(), name='post_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',
        views.post_detail, name='post_detail'),
    url(r'^(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),
    url(r'^login/$', login, name='login'),
    #url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^logout-then-login/$', views.logout_then_login_view,
        name='logout_then_login'),
    url(r'^dashboard', views.dashboard, name='dashboard'),
    #url(r'^password-change/$', views.password_change, name='password_change'),
    #url(r'^password-change/done/$', views.password_change_done, name='password_change_done'),
    url(r'^password-change/$', password_change, 
        {'template_name': 'registration/password_change_form.html'}, name='password_change'),
    url(r'^password-change/done/$', password_change_done,
        {'template_name': 'registration/password_change_done.html'}, name='password_change_done'),
    url(r'^password-reset/$', password_reset, name='password_reset'),
    url(r'^password-reset/done/$', password_reset_done,
        name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        password_reset_confirm, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', password_reset_complete,
        name='password_reset_complete'),
    url(r'^register/$', views.register, name='register'),
    url(r'^edit/$', views.edit, name='edit'),
]
