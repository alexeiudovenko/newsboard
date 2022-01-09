from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Post, Comment, Voted
from .forms import RegisterForm



class RegisterView(generic.CreateView):
    template_name = "newsboard/register.html"
    success_url = reverse_lazy("newsboard:login")
    form_class = RegisterForm


class NewsView(generic.ListView):
    template_name = "newsboard/index.html"
    context_object_name = "post"
    queryset = Post.objects.order_by("-id")


class CommentView(generic.CreateView):
    model = Comment
    template_name = "newsboard/comments.html"
    context_object_name = "comment"
    fields = ["author_name_comment", "content"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment"] = self.model.objects.filter(
            post_comment_id=self.kwargs["pk"]
        ).order_by("-id")
        return context

    def form_valid(self, form):
        form.instance.post_comment_id = self.kwargs["pk"]
        return super().form_valid(form)

    def get_success_url(self):
        success_url = reverse_lazy("newsboard:comments", args=(self.kwargs["pk"],))
        return success_url


@login_required(login_url="/login/")
def Vote(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        if not Voted.objects.filter(
            user_voted=request.user, post_voted=post, voted=True
        ):
            v = Voted(user_voted=request.user, post_voted=post, voted=True)
            v.save()
            post.votes = F("votes") + 1
            post.save()
    return HttpResponseRedirect(reverse("newsboard:news"))


@login_required(login_url="/login/")
def ResetVote(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        Voted.objects.filter(post_voted=post, voted=True).delete()
        post.votes = F("votes") * 0
        post.save()
    return HttpResponseRedirect(reverse("newsboard:news"))
