from django.db import models
from authenticate.models import User


class NewsManager(models.Manager):
    def for_user(self, user):
        return self.filter(editor=user)


class Category(models.Model):
    category = models.CharField(max_length=250)
    parent_categories = models.ManyToManyField(
        'self', symmetrical=False, blank=True, related_name='child_categories')

    def __str__(self):
        return self.category


class News(models.Model):
    editor = models.ForeignKey(User, on_delete=models.CASCADE)
    news_img = models.ImageField(upload_to="news")
    title = models.CharField(max_length=200)
    card_title = models.CharField(max_length=50, blank=True)
    short_description = models.CharField(max_length=500, blank=True)
    long_description = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    link = models.URLField()
    keywords = models.CharField(max_length=500)
    category = models.ManyToManyField(Category)

    objects = NewsManager()
