from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path

router = DefaultRouter()
router.register(r"posts", views.PostViewSet, basename="post")
router.register(r"comments", views.CommentViewSet, basename="comment")
urlpatterns = [
    path("vote", views.VotedViewSet.as_view({"post": "create"})),
    path("vote/reset/<int:pk>", views.ResetVotedViewSet.as_view({"get": "delete_all"})),
] + router.urls
