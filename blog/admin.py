from django.contrib import admin
from .models import Post, Category, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'author', 'created_at', 'is_approved']
    list_filter = ['category']
    search_fields = ['title', 'content']
    def approve_post(self, request, queryset):
        queryset.update(is_approved=True)

    approve_post.short_description = 'Tasdiqlash'

    actions = [approve_post]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'content', 'created_at']
