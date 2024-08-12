from django.contrib import admin
from users.models import User, FriendRequest

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username','first_name','last_name']

@admin.register(FriendRequest)
class UserAdmin(admin.ModelAdmin):
    list_display = ['from_user','to_user','status','created_at']



