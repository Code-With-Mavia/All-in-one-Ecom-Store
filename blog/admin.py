# admin.py
from django.contrib import admin
from .models import BlogPost, Tag, AboutRating, AboutComment

# ----- Tag Admin -----
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

# ----- BlogPost Admin -----
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('created_at', 'tags')
    search_fields = ('title', 'author', 'content')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)

# ----- AboutRating Admin -----
@admin.register(AboutRating)
class AboutRatingAdmin(admin.ModelAdmin):
    list_display = ('rating', 'created_at')
    ordering = ('-created_at',)

# ----- AboutComment Admin -----
@admin.register(AboutComment)
class AboutCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date_posted')
    ordering = ('-date_posted',)
