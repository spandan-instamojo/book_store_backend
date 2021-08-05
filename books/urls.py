from django.urls import path, include
from django.conf.urls import url
from django.urls import path
from .views import CategoryBooksView, BookView, CategoryListView, create

urlpatterns = [
    path(r'category', CategoryListView.as_view()),
    path(r'category-books/<int:category>', CategoryBooksView.as_view()),
    path(r'<int:pk>', BookView.as_view()),
    path(r'create', create)

]
