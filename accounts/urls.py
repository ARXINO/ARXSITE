from django.conf.urls import url
from . import views
from django.contrib.auth.views import (
    login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
    )


urlpatterns = [
    url(r'^$', views.home),
    url(r'^login/$', login, {'template_name':'accounts/login.html'}),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^howtoplay/$', views.nasiloynanir, name = 'nasiloynanir'),
    url(r'^about-us/$', views.hakkimizda, name = 'hakkimizda'),
    url(r'^register/hatali_form$', views.hatali_form, name = 'hatali_form'),
    url(r'^game/$', views.game, name = 'game'),
    url(r'^message/$', views.message, name = 'message'),
    url(r'^announcement/$', views.announcement, name = 'announcement'),
    url(r'^game/game_menu$', views.game_menu, name = 'game_menu'),
    url(r'^game/game_bayir$', views.game_bayir, name = 'game_bayir'),
    url(r'^game/game_bahce$', views.game_bahce, name = 'game_bahce'),
    url(r'^profile/$', views.profile, name = 'profile'),
    url(r'^profile_karakter/$', views.profile_karakter, name = 'profile_karakter'),
    url(r'^profile/edit$', views.edit_profile, name = 'edit_profile'),
    url(r'^password/$', views.change_password, name = 'change_password'),
    url(r'^reset-password/$', password_reset, name = 'reset_password'),
    url(r'^reset-password/done/$', password_reset_done, name = 'password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', password_reset_complete, name='password_reset_complete'),
]


