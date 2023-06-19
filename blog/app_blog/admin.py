from django.contrib import admin
from app_blog.models import Post, Comment

admin.site.register(Post)
admin.site.register(Comment)