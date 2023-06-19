from django.http import HttpResponseRedirect
from django.shortcuts import render
from app_blog.models import Post, Comment
from django.urls import reverse

from .forms import CommentForm


def home(request):
    d = {}
    posts = None
    try:
        posts = Post.objects.all()
    except Exception as ex:
        assert ex
    d["posts"] = posts
    return render(request, 'blog/home.html', context=d)


def post(request, post_id):
    d = {}
    post_obj = None
    comments = None
    comment_form = CommentForm()
    if request.method == 'GET':
        try:
            post_obj = Post.objects.get(id=post_id)
            comments = Comment.objects.filter(post_id=post_id)
        except Exception as ex:
            assert ex
        d["comment_form"] = comment_form
    if request.method == "POST" and "comment" in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            content = comment_form.cleaned_data["content"]
            comment = Comment()
            comment.content = content
            comment.author = request.user
            comment.post = Post.objects.get(id=post_id)
            comment.save()
            return HttpResponseRedirect(f"/post/{post_id}")
    d["post"] = post_obj
    d["comments"] = comments
    return render(request, 'post/post.html', context=d)
