from django.shortcuts import render
from watchlist.models import Movies
from django.http import JsonResponse


def movie_list(request):
    movies = Movies.objects.all()
    data = {
        'movies' : list(movies.values())
        }

    return JsonResponse(data)


def movie_details(request, pk):
    movie = Movies.objects.get(pk=pk)
    data = {
        'title' : movie.title,
        'description' : movie.description,
        'active' : movie.active
    }

    return JsonResponse(data)

