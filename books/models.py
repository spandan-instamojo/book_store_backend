from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    @property
    def category_code(self):
        return self.name[:3].upper()


class Book(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    description = models.TextField()

    class Meta:
        ordering = ['title']

    @property
    def bookid(self):
        return "{}-{}".format(self.category.category_code, self.id)

