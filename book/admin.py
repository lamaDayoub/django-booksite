from django.contrib import admin
from .models import UserBookRelation,Book
# Register your models here.
admin.site.register(UserBookRelation)
admin.site.register(Book)