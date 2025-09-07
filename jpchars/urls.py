from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("get_levels", views.get_levels, name="get_levels"),
    path("get_exercises", views.get_exercises, name="get_exercises"),
    path("get_tasks/<str:type>/<int:level>", views.get_tasks, name="get_tasks"),
    path("update_level", views.update_level, name="update_level")
]