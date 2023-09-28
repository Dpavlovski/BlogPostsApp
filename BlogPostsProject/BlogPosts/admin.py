from django.contrib import admin
from .models import *


# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        if obj and obj.user == request.user:
            return True
        return False


admin.site.register(UserProfile, UserProfileAdmin)


class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "author"]
    search_fields = ["title", "content"]
    list_filter = ["creation_date"]
    exclude = ["user"]

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        if obj and obj.user == request.user or request.user.is_superuser:
            return True
        return False

    def has_view_permission(self, request, obj=None):
        return obj and not BlockUser.objects.filter(blocker__user=obj.post.author.user,
                                                    blocked__user=request.user).exists()

    def save_model(self, request, obj, form, change):
        if obj:
            obj.user = UserProfile.objects.get(user=request.user)

        super().save_model(request, obj, form, change)


admin.site.register(Blog, BlogAdmin)


class FileAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return obj and request.user == obj.blog.author

    def has_delete_permission(self, request, obj=None):
        return obj and request.user == obj.blog.author

    def has_view_permission(self, request, obj=None):
        return obj and not BlockUser.objects.filter(blocker__user=obj.post.author.user,
                                                    blocked__user=request.user).exists()


admin.site.register(File, FileAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ["content", "creation_date"]
    exclude = ["user"]

    def has_add_permission(self, request):
        return not request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return obj and not BlockUser.objects.filter(blocker__user=obj.post.author.user,
                                                    blocked__user=request.user).exists()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return obj and (request.user == obj.user or request.user == obj.post.author)

    def save_model(self, request, obj, form, change):
        if obj:
            obj.user = UserProfile.objects.get(user=request.user)

        super().save_model(request, obj, form, change)


admin.site.register(Comment, CommentAdmin)


class BlockUserAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return obj and request.user == obj.blocker.user

    def has_delete_permission(self, request, obj=None):
        return obj and request.user == obj.blocker.user


admin.site.register(BlockUser, BlockUserAdmin)
