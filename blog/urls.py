from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.new_post, name='new_post'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('pending_posts/', views.pending_posts, name='pending_posts'),
    path('approve_post/<int:pk>/', views.approve_post, name='approve_post'),
]
