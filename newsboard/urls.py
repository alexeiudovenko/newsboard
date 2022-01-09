from django.urls import path
from .views import NewsView, CommentView, Vote, ResetVote, RegisterView
from django.contrib.auth.views import LoginView, LogoutView


app_name = "newsboard"
urlpatterns = [
    path("", NewsView.as_view(), name="news"),
    path(
        "login/", LoginView.as_view(template_name="newsboard/login.html"), name="login"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("comments/<int:pk>", CommentView.as_view(), name="comments"),
    path("vote/<int:pk>", Vote, name="vote"),
    path("resetvote/<int:pk>", ResetVote, name="resetvote"),
]
