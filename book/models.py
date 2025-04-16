from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
# Create your models here.
class Book(models.Model):
    title=models.CharField( max_length=100)
    author=models.CharField(max_length=100)
    readers=models.ManyToManyField('users.User', through=("UserBookRelation"), related_name='tracked_books')
    class Meta:
        unique_together =['title','author']   
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    
class UserBookRelation(models.Model):
    user=models.ForeignKey('users.User',  on_delete=models.CASCADE, related_name='book_relations')
    book=models.ForeignKey(Book,  on_delete=models.CASCADE,related_name='user_relations')
    shelf = models.CharField(max_length=20, choices=[
        ('WANT_TO_READ', 'Want to Read'),
        ('READING', 'Currently Reading'),
        ('READ', 'Finished'),
        ('FAVOURITE','Favourite'),
    ],
                             default='WANT_TO_READ'
                             )
    rating=models.PositiveSmallIntegerField(null=True,blank=True,validators=[
            MinValueValidator(1),  # Must be ≥ 1
            MaxValueValidator(5)   # Must be ≤ 5
        ])
    class Meta:
        unique_together = ['user', 'book'] 
    def __str__(self):
        return f"{self.user.username}'s {self.book.title}: {self.shelf}"
