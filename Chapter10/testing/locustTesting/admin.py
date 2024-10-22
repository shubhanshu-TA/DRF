from django.contrib import admin

# Register your models here.

from .models import Post, Comment

admin.site.register(Comment)
admin.site.register(Post)
