from django.contrib import admin
from .models import Profile, BlogPost

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('description', 'user__username')
