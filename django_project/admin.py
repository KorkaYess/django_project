from django.contrib import admin
from django.utils.html import format_html

from .models import Profile, Post, Follower


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    def avatar_tag(self, obj):
        try:
            return format_html(
                '<img src="{}" width="100" height="100" />'.format(obj.avatar.url)  # noqa
            )
        except:  # noqa
            pass

    avatar_tag.short_description = 'Avatar'
    list_display = [
        'avatar_tag', 'first_name', 'last_name', 'birthday', 'direction',
        'city', 'phone', 'website', 'age', 'zodiac'
    ]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html(
            '<img src="{}" width="100" height="100" />'.format(obj.image.url)
        )

    image_tag.short_description = 'Image'
    list_display = ['profile', 'image_tag', 'description', 'created']


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following']
