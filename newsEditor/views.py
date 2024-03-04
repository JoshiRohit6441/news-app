from .models import News, Category
from .serializer import NewsSerializer, CategorySerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import permissions as rest_permissions

from rest_framework import viewsets


class CategoryView(APIView):
    permission_classes = [rest_permissions.AllowAny]

    def get(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.save():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsView(APIView):
    permission_classes = [rest_permissions.IsAuthenticated]

    def get(self, request, id=None):
        user = request.user

        if id:
            news = News.objects.filter(editor=user, id=id).first()
            if news:
                serializer = NewsSerializer(news)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("News not found", status=status.HTTP_404_NOT_FOUND)
        else:
            news = News.objects.filter(editor=user)
            serializer = NewsSerializer(news, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['editor'] = request.user.id
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        user = request.user
        news = News.objects.filter(editor=user, id=id).first()
        if not news:
            return Response("News not found", status=status.HTTP_404_NOT_FOUND)

        serializer = NewsSerializer(news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        user = request.user
        news = News.objects.filter(editor=user, id=id).first()
        if not news:
            return Response("News not found", status=status.HTTP_404_NOT_FOUND)

        news.delete()
        return Response("News deleted successfully", status=status.HTTP_200_OK)


class AllNews(APIView):
    permission_classes = [rest_permissions.AllowAny]

    def get(self, request):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
