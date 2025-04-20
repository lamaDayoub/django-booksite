# books/serializers.py
from rest_framework import serializers
from .models import UserBookRelation,Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=['id','title','author']
        

class UserBookRelationSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), write_only=True)
    book_details = BookSerializer(source='book', read_only=True)

    class Meta:
        model = UserBookRelation
        fields = ['id', 'book', 'book_details','shelf', 'rating']
        extra_kwargs = {
            'rating': {'required': False, 'allow_null': True}  # Allow null but validate later
        }

    def validate(self, data):
        
        shelf = data.get('shelf')
        rating = data.get('rating')  
        rating_missing = rating is None or rating == ''

        
        if shelf in ['READ', 'FAVOURITE'] and rating_missing:
            
            if self.instance and self.instance.rating is not None:
                
                pass
            else:
                raise serializers.ValidationError(
                    {"rating": "Rating is required for Read and Favorite shelves."}
                )

        
        if rating not in [None, '']:
            try:
                rating_int = int(rating)
                if rating_int < 1 or rating_int > 5:
                    raise serializers.ValidationError({
                        "rating": "Rating must be between 1 and 5."
                    })
            except (ValueError, TypeError):
                raise serializers.ValidationError({
                    "rating": "Rating must be a valid integer."
                })

        return data