from django.contrib import admin

from knowme.posts.models import Post, Report


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['photo', 'profile', 'description', 'location']


@admin.register(Report)
class PostReportAdmin(admin.ModelAdmin):
    list_display = ['text', 'to_post_id', 'profile_id']
