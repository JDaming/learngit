from django.db import models

# Create your models here.
class Book(models.Model):
    ISBN = models.CharField(max_length = 13, primary_key = True)
    Title = models.CharField(max_length = 100)
    AuthorID = models.ForeignKey("Author")
    Publisher = models.CharField(max_length = 100)
    PublishDate = models.DateField()
    Price = models.CharField(max_length = 5)
class Author(models.Model):
    AuthorID = models.CharField(max_length = 10, primary_key = True)
    Name = models.CharField(max_length = 20)
    Age = models.DateField()
    Country = models.CharField(max_length = 20)
