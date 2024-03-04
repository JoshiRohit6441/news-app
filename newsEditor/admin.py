from django.contrib import admin
from .models import News, Category
from django.utils.html import format_html


class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "editor", "card_title", "pic", "link")

    def pic(self, obj):
        if obj.news_img:
            return format_html('<img src="{}" style="max-width:50px; max-height:50px"/>'.format(obj.news_img.url))
        else:
            return None


admin.site.register(News, NewsAdmin)

admin.site.register(Category)
