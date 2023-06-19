from django.urls import re_path, path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('post/<int:post_id>', views.post, name='post'),

]
