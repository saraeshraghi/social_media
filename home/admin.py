from django.contrib import admin
from .models import Post, Relations, Comment, Vote


class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'update')
    search_fields = ('slug', 'user')
    list_filter = ('update',)
    prepopulated_fields = {'slug': ('body',)}
    # raw_id_fields = ('user',)


admin.site.register(Post, PostAdmin)
admin.site.register(Relations)
admin.site.register(Vote)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'body', 'created', 'is_reply')
    raw_id_fields = ('user', 'post', 'reply')
