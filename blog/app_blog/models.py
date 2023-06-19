from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    date_posted = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, null=True)
    author = models.ForeignKey('auth.User', related_name='author', on_delete=models.CASCADE, null=True)
    content = models.TextField("Комментарий")
    date_posted = models.DateField(auto_now=True)
