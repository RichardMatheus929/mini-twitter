from django.contrib import admin
from twitter.follow.models import Follow

# Register your models here.
from django.contrib import admin

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)  # <-- Torna o ID visível e somente leitura