from django.contrib import admin
from .models import Post, Comment, Profile


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created_at', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created_at', 'active')
    list_filter = ('active', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'body')

admin.site.register(Comment, CommentAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
    
admin.site.register(Profile, ProfileAdmin)