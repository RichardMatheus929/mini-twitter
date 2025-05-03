from django.contrib import admin
from twitter.likes.models import Like

# Register your models here.
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)