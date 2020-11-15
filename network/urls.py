
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts/<str:mode>/<str:where>/<int:user_id>", views.show10Posts, name='show10Posts'),
    path("makeLike", views.makeLike, name='makeLike'),
    path("user/<int:user_id>", views.getUserPage, name='userPage'),
    path("follow/<str:user_page>", views.changeFollow, name='followUser'),
    path("edit/<int:post_id>", views.editPost, name='editPost'),
    path("following", views.followingPage, name="followingPage")
]
