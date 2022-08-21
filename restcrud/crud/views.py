from math import perm
from os import access
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, APIView
from crud.serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Movie, Review
from .serializers import MovieListSerializer, ReviewListSerializer

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
import jwt
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken



# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    token = RefreshToken(request.data.get('refresh'))
    token.blacklist()

    return Response("Success")

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def movie_list_create(request):

    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieListSerializer(movies, many=True)

        return Response(data=serializer.data)

    if request.method == 'POST':

        serializer = MovieListSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def movie_detail_update_delete(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    if request.method=='GET':
        serializer = MovieListSerializer(movie)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = MovieListSerializer(instance=movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        movie.delete()
        data = {
            'movie':movie_pk
        }
        return Response(data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def review_list_create(request, movie_pk):
    _movie = Movie.objects.get(pk = movie_pk)

    if request.method == 'GET':

        reviews = Review.objects.filter(movie = _movie)
        serializer = ReviewListSerializer(reviews, many=True)

        return Response(data=serializer.data)

    if request.method == 'POST':
        request.data['movie'] = movie_pk

        serializer = ReviewListSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data)

@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def review_detail_update_delete(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    if request.method == 'GET':
        serializer = ReviewListSerializer(review)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        request.data['movie'] = movie_pk

        serializer = ReviewListSerializer(instance=review, data=request.data)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)

    elif request.method == 'DELETE':
        review.delete()
        data = {
            'review' : review_pk
        }

        return Response(data)

@api_view(["POST"])
@permission_classes([AllowAny])
def user_regist(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)

@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        expired_at = (timezone.now() + timedelta(days=14)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        access_token = jwt.encode(
            {"user_id" :user.id, "expired_at" : expired_at},settings.SECRET_KEY
        )
        return Response(access_token)
    return Response("Invalid username or password", status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def test(request):
    return Response(request.user.username)

    

