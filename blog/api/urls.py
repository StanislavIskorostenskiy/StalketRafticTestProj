from django.urls import re_path, path

from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    path('posts', views.posts),
    path('post/<int:post_id>', views.post_by_id),
    path('create_post', views.create_post),
    path('signIn', views.signIn),
    path('signUp', views.signUp),

]
