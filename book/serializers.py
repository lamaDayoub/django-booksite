# books/serializers.py
from rest_framework import serializers
from .models import UserBookRelation,Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=['id','title','author']
        

class UserBookRelationSerializer(serializers.ModelSerializer):
    book=BookSerializer()
    class Meta:
        model = UserBookRelation
        fields = ['id', 'book', 'shelf', 'rating']
        extra_kwargs = {
            'rating': {'required': False}  
        }
    
    
    def validate(self, data):
        user = self.context['request'].user
        book = data.get('book') or getattr(self.instance, 'book', None)
        shelf = data.get('shelf')
        rating = data.get('rating')
        # Get existing shelf status if updating
        existing = self.instance.shelf if hasattr(self, 'instance') and self.instance else None
        
        incompatible_shelves={
            'WANT_TO_READ':['FAVOURITE','READ'],
            'READ':['WANT_TO_READ'],
            'FAVOURITE':['WANT_TO_READ']
        }
        if existing in incompatible_shelves.get(shelf,[]):
            raise serializers.ValidationError(
                f"Cannot move from {existing} to {shelf} shelf"
            )

        if shelf in ['READ', 'FAV'] and 'rating' not in data:
            if not (self.instance and self.instance.rating):
                raise serializers.ValidationError(
                    {"rating": "Required for Read and Favorite shelves"}
                )
        
        return data