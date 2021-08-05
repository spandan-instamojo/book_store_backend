from django.shortcuts import render
from django.http import Http404
from rest_framework import views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import Category, Book
from rest_framework import status
# Create your views here.
from .serializers import CategorySerializer, BookSerializer


class CategoryBooksView(ListAPIView):
    model = Book
    serializer_class = BookSerializer

    def get_queryset(self):
        category = self.kwargs.get('category')
        return Book.objects.filter(category_id=category)


class CategoryListView(ListAPIView):
    model = Category
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class BookView(views.APIView):

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        book = self.get_object(pk=kwargs.get('pk'))
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        book = self.get_object(kwargs.get('pk'))
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        book = self.get_object(kwargs.get('pk'))
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['category_id'] = request.data['category']
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)