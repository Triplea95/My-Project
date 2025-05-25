from django.shortcuts import render, get_object_or_404
from rest_framework import status, generics,filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import NewsItem
from .serializers import NewsItemCreateSerializer, NewsItemSerializer
from django.db.models import Q
from .permissions import IsVerifiedUser
from rest_framework.permissions import IsAuthenticated 



class NewsItemCreateView(APIView):
    permission_classes = [IsAuthenticated, IsVerifiedUser]

    def post(self, request):
        serializer = NewsItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



class NewsItemListCreateView(APIView):
    def get(self, request):
        news_item = NewsItem.objects.all()  # start with all items

        # Search
        search = request.query_params.get('search')
        if search:
            news_item = news_item.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(author__username__icontains=search) |
                Q(category__name__icontains=search) |
                Q(tags__name__icontains=search)
            ).distinct()

        # Filter by category
        category = request.query_params.get('category')
        if category:
            news_item = news_item.filter(category__id=category)

        # Filter by author
        author = request.query_params.get('author')
        if author:
            news_item = news_item.filter(author__id=author)

        # Ordering
        ordering = request.query_params.get('ordering')
        if ordering:
            news_item = news_item.order_by(ordering)
        else:
            news_item = news_item.order_by('published_date')

        serializer = NewsItemSerializer(news_item, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required to create news."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = NewsItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsItemDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk): 
        news_item = get_object_or_404(NewsItem, pk=pk)

    # pk means Primary Key
        # Check if the requesting user is the author/reporter
        if news_item.author != request.user:
            return Response({"detail": "You do not have permission to delete this news item."},
                            status=status.HTTP_403_FORBIDDEN)

        news_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

