from .models import News, Category
from rest_framework import serializers
from authenticate.serializer import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category"]


class NewsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    editor = UserSerializer(many=False)

    class Meta:
        model = News
        fields = "__all__"
