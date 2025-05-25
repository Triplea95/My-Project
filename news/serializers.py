from rest_framework import serializers
from .models import NewsItem

class NewsItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = ['title', 'content', 'categories', 'tags', 'is_published']

    def create(self, validated_data):
        # Automatically set the author to the logged-in user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
    


class NewsItemSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)  # Display username
    slug = serializers.ReadOnlyField()  # In case you're using AutoSlugField

    class Meta:
        model = NewsItem
        fields = [
            'id',
            'title',
            'slug',
            'category',
            'tags',
            'author'
        ]
        read_only_fields = ['author', 'slug', 'created_at']

    def create(self, validated_data):
        # Automatically assign the current user as the author
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
