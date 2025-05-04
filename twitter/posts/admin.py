from django.contrib import admin

from twitter.posts.models import Post

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)