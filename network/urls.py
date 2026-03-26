
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-post", views.new_post, name="new_post"),
    path("profile/<int:user_pk>", views.profile, name="profile"),
    path("follow/<int:user_pk>", views.follow, name="follow"),
    path("following", views.following, name="following"),

    # API Routes
    path("posts/<int:post_pk>", views.post, name="post")

]
