from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from app_blog.models import Post, Comment
from api.serializer import PostSerializer, SignInSerializer, SignUpSerializer
from django.contrib.auth.models import User
import json


@api_view(["POST"])
def create_post(request):
    if request.method == "POST" and request.user.is_supperuser():
        data = request.data
        post = Post()
        post.title = data["title"]
        post.content = data["content"]
        post.author = request.user
        post.save()
        data = {"post_id": post.id}
        return JsonResponse(data, status=200, safe=False)
    return HttpResponse(status=500)


@api_view(["GET"])
def posts(request):
    if request.method == 'GET':
        posts_obj = None
        try:
            posts_obj = Post.objects.all()
        except Exception as ex:
            assert ex
        if posts_obj is not None:
            serializer = PostSerializer(posts_obj, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
        return HttpResponse(status=500)


@api_view(["GET"])
def post_by_id(request, post_id):
    if request.method == 'GET':
        posts_obj = None
        try:
            posts_obj = Post.objects.get(id=post_id)
        except Exception as ex:
            assert ex
        if posts_obj is not None:
            serializer = PostSerializer(posts_obj)
            return JsonResponse(serializer.data, status=200, safe=False)
        return HttpResponse(status=500)


@api_view(["POST"])
def create_comment(request, post_id):
    if request.method == "POST" and request.user.is_authenticated():
        data = request.data
        post = Post.objects.get(id=post_id)
        comment = Comment()
        comment.post = post
        comment.content = data["content"]
        comment.author = request.user
        comment.save()
        data = {"comment_id": comment.id}
        return JsonResponse(data, status=200, safe=False)
    return HttpResponse(status=500)


@api_view(["POST"])
def signIn(request):
    if request.method == "POST":
        body = json.loads(request.body)
        username = body['username']
        password = body['password']
        user = authenticate(request, username=username, password=password)
        serializer = SignInSerializer(data=body)
        if user is not None:
            login(request, user)
            if serializer.is_valid():
                return JsonResponse(serializer.data, status=200, safe=False)
        return HttpResponse(status=500)


@api_view(["POST"])
def signUp(request):
    if request.method == "POST":
        data = list(request.data.keys())[0]
        data = json.loads(data)
        username = data.get("username")
        serializer = SignUpSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=username)
            login(request, user)
            return JsonResponse(serializer.data, status=200, safe=False)
        return HttpResponse(status=500)
