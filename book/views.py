from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book, UserBookRelation
from .serializers import BookSerializer, UserBookRelationSerializer
from django.db import models
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.
class BookshelveView(APIView):
    permission_classes = [IsAuthenticated] 
    authentication_classes = [JWTAuthentication]
    @swagger_auto_schema(
        operation_id='book_list',  # Add this unique identifier
        tags=['Books'],
        operation_description="Add or update a book on user's shelf",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['book', 'shelf'],
            properties={
                'book': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    required=['title', 'author'],
                    properties={
                        'title': openapi.Schema(type=openapi.TYPE_STRING),
                        'author': openapi.Schema(type=openapi.TYPE_STRING),
                        
                    }
                ),
                'shelf': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['WANT_TO_READ', 'READING', 'READ', 'FAVOURITE'],
                    description="Shelf to place the book on. Rating is required if shelf is READ or FAVORITE"
                ),
                'rating': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    minimum=1,
                    maximum=5,
                    nullable=True,
                    description="Required if shelf is READ or FAVOURITE, otherwise optional"
                )
            },
            # Add this for conditional requirement
            if_properties={
                'shelf': {
                    'enum': ['READ', 'FAVOURITE']
                }
            },
            then_properties={
                'rating': {
                    'required': True
                }
            }
        ),
        responses={
            201: openapi.Response("Book added to shelf", UserBookRelationSerializer),
            200: openapi.Response("Book shelf status updated", UserBookRelationSerializer),
            400: openapi.Response("Invalid input", schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING),
                    'details': openapi.Schema(type=openapi.TYPE_OBJECT)
                }
            )),
            401: "Authentication required"
        },
        security=[{"Bearer": []}]
    )
    
    def post(self,request):
        book_data=request.data.get('book')
        book,created=Book.objects.get_or_create(
            title=book_data['title'],
            author=book_data['author'],
            defaults=book_data
            
        )
        
        user_book,created=UserBookRelation.objects.update_or_create(
            user=request.user,
            book=book,
            defaults={
                'shelf': request.data['shelf'],
                'rating':request.data.get('rating')
            }
        )
        serializer=UserBookRelationSerializer(user_book)
        return Response(serializer.data, 
                        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        
class BookList(APIView):
    permission_classes = [IsAuthenticated] 
    authentication_classes = [JWTAuthentication]
    @swagger_auto_schema(
        operation_id='book_list',  # Add this unique identifier
        tags=['Books'],
        operation_description="List all books with optional search and shelf filtering",
        manual_parameters=[
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                description="Search by book title or author (case-insensitive)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='shelf',
                in_=openapi.IN_QUERY,
                description="Filter by shelf status (requires authentication)",
                type=openapi.TYPE_STRING,
                enum=['WANT_TO_READ', 'READING', 'READ', 'FAVOURITE']
            )
        ],
        responses={
            200: openapi.Response(
                description="List of books",
                schema=BookSerializer(many=True))
        },
        security=[{"Bearer": []}]
    )
    def get(self,request):
        queryset=Book.objects.all()
        
        search_query=request.query_params.get('search')
        if search_query:
            queryset=queryset.filter(
                models.Q(title__icontains=search_query) |
                models.Q(author__icontains=search_query)
            )
        shelf=request.query_params.get('shelf')
        if shelf:
            queryset = queryset.filter(
                user_relations__user=request.user,
                user_relations__shelf=shelf
            )
        
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)
    
class BookDetailView(APIView):
    permission_classes = [IsAuthenticated] 
    authentication_classes = [JWTAuthentication]
    @swagger_auto_schema(
        operation_id='book_list_by_shelf_or_not',
        tags=['Books'],
        operation_description="Get book details with user's shelf status",
        responses={
            200: openapi.Response(
            description="Success",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'book': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'title': openapi.Schema(type=openapi.TYPE_STRING),
                            'author': openapi.Schema(type=openapi.TYPE_STRING)
                        }
                    ),
                    'user_status': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'book': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'title': openapi.Schema(type=openapi.TYPE_STRING),
                                    'author': openapi.Schema(type=openapi.TYPE_STRING)
                                }
                            ),
                            'shelf': openapi.Schema(type=openapi.TYPE_STRING),
                            'rating': openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True)
                        },
                        nullable=True
                    )
                }
            )
        ),
        404: "Book not found"
        },
        security=[{"Bearer": []}]
    )
    
    def get(self, request, id=None):
        book = get_object_or_404(Book, id=id)
        
        user_relation = None
        if request.user.is_authenticated:
            user_relation = UserBookRelation.objects.filter(
                user=request.user,
                book=book
            ).first()
            
        response_data = {
            'book': BookSerializer(book).data,
            'user_status': UserBookRelationSerializer(user_relation).data if user_relation else None
        }
        
        return Response(response_data)