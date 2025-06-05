from django.urls import path
from . import views_blog

urlpatterns = [
    path('', views_blog.blog_home, name='blog_home'),
    path('post/<slug:slug>/', views_blog.blog_post_detail, name='blog_post_detail'),
    path('post/<int:pk>/edit/', views_blog.blog_post_edit, name='blog_post_edit'),
    path('post/<slug:slug>/delete/', views_blog.blog_post_delete, name='blog_post_delete'),
    path('create/', views_blog.blog_post_create, name='blog_post_create'),
    path('about/', views_blog.blog_about, name='blog_about'),
    path('contact/', views_blog.blog_contact, name='blog_contact'),
    path('tag/<slug:tag_slug>/', views_blog.blog_posts_by_tag, name='blog_posts_by_tag'),

    # POST endpoints for rating and comments
    path('post/<slug:slug>/add-rating/', views_blog.add_rating, name='add_rating'),
    path('post/<slug:slug>/add-comment/', views_blog.add_comment, name='add_comment'),
]
