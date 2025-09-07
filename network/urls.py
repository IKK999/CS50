
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('new_post', views.new_post, name='new_post'),
    path('posts/<str:section>/<int:page>/<str:name>', views.section, name='posts'),
    path('following', views.following, name='following'),
    path('profile/<str:author>', views.profile, name='profile'),
    path('follow_count/<str:author>', views.follow_count, name='follow_count'),
    path('follow_status/<str:author>', views.follow_status, name='follow_status'),
    path('flip_status/<str:author>', views.flip_status, name='flip_status'),
    path('pages_present/<str:section>/<int:page>/<str:name>', views.pages_present, name='pages_present'),
    path('edit_post/<str:section>/<int:page>/<str:name>/<int:i>', views.edit_post, name='edit_post'),
    path('switch_status/<str:section>/<int:page>/<str:name>/<int:i>', views.switch_status, name='switch_status'),
    path('is_liked/<str:section>/<int:page>/<str:name>/<int:i>', views.is_liked, name='is_liked')
]
