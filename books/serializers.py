from rest_framework import serializers
from .models import Category, Book


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

    def validate(self, attrs):
        return attrs


