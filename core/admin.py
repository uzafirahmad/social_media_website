from django.contrib import admin
from .models import Accounts,sections,subsections,posts,followerslist,followinglist,ChatModel,ChatFather,notifications
from django.contrib.auth.admin import UserAdmin
import nested_admin

#Register your models here.
class NotificationAdmin(nested_admin.NestedStackedInline):
    model=notifications
    extra=0
    list_display=('notification_owner','notification_text','notification_read')
    readonly_fields=('notification_id','notification_image','notification_date')

class FollowingListAdmin(nested_admin.NestedTabularInline):
    model=followinglist
    extra=0
    list_display=('fuser','email')

class FollowerListAdmin(nested_admin.NestedTabularInline):
    model=followerslist
    extra=0
    list_display=('fuser','email')

class PostsAdmin(nested_admin.NestedStackedInline):
    model=posts
    extra=0
    list_display=('post_time','post_text','post_image','post_video','post_owner')
    readonly_fields=('post_owner','post_time')

class SubsectionsAdmin(nested_admin.NestedStackedInline):
    inlines=[PostsAdmin]
    model=subsections
    extra=0
    # list_display=('subsection_serial','subsection_add_date','subsection_owner')
    # readonly_fields=('subsection_add_date','subsection_owner')

class SectionAdmin(nested_admin.NestedStackedInline):
    inlines=[SubsectionsAdmin]
    model=sections
    extra=0
    list_display=('section_owner','section_name','viewable_to','sec_description')
    readonly_fields=('section_owner',)

class AccountAdmin(UserAdmin,nested_admin.NestedModelAdmin):
    inlines=[SectionAdmin,FollowerListAdmin,FollowingListAdmin,NotificationAdmin]
    list_display=('email','username','date_joined','last_login','is_admin','is_staff')
    search_fields=('email','username')
    readonly_fields=('id','date_joined','last_login')
    filter_horizontal=()
    list_filter=()
    fieldsets=()

# Chat Models
class ChatModelAdmin(admin.StackedInline):
    model=ChatModel
    extra=0
    list_display=('sender','message','timestamp')
    readonly_fields=('timestamp','sender','message_id')

class ChatFatherAdmin(admin.ModelAdmin):
    inlines=[ChatModelAdmin]
    model=ChatFather
    extra=0
    list_display=['thread_name']

admin.site.register(Accounts,AccountAdmin)
admin.site.register(ChatFather,ChatFatherAdmin)