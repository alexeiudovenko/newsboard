from rest_framework import viewsets
from .serializers import PostSerializer, CommentSerializer, VotedSerializer
from newsboard.models import Post, Comment, Voted
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F
from django.shortcuts import get_object_or_404


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.order_by("-id")


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.order_by("-id")


class VotedViewSet(viewsets.ModelViewSet):
    serializer_class = VotedSerializer
    queryset = Voted.objects.all()


class ResetVotedViewSet(viewsets.ModelViewSet):
    serializer_class = VotedSerializer
    queryset = Voted.objects.all()

    @action(detail=False, methods=["get"])
    def delete_all(self, request, pk):
        if request.method == "GET":
            post = get_object_or_404(Post, pk=pk)
            Voted.objects.filter(post_voted=post, voted=True).delete()
            post.votes = F("votes") * 0
            post.save()
        return Response("success")
