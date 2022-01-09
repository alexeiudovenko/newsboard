from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    link = models.URLField(verbose_name="Link")
    creation_date = models.DateField(
        verbose_name="Creation Date", default=datetime.today().date()
    )
    votes = models.IntegerField(verbose_name="Votes", default=0)
    author_name = models.CharField(verbose_name="Author Name", max_length=50)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post_comment = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comment"
    )
    author_name_comment = models.CharField(verbose_name="Author Name", max_length=50)
    content = models.TextField(max_length=150, verbose_name="Content")
    creation_date_comment = models.DateField(
        verbose_name="Creation Date", default=datetime.today().date()
    )

    def __str__(self):
        return self.author_name_comment


class Voted(models.Model):
    user_voted = models.ForeignKey(User, on_delete=models.CASCADE, default=User)
    post_voted = models.ForeignKey(Post, on_delete=models.CASCADE)
    voted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.post_voted)
