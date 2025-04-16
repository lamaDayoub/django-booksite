from django.contrib import admin
from .models import User,UserPasswordHistory
#Register your models here.
admin.site.register(User)


@admin.register(UserPasswordHistory)
class UserPasswordHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__email',)