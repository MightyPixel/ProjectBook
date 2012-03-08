from django.contrib import admin

from projectbook.apps.wall.models import Post
from projectbook.apps.wall.models import Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 3


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
            (None,               {'fields': ['title' , 'body']}),
            ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ]
    inlines = [CommentInline]
    list_display = ('title', 'pub_date', 'was_published_today')
    list_filter = ['pub_date']
    
    search_fields = ['title']
    date_hierarchy = 'pub_date'

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
