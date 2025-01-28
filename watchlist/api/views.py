from rest_framework.response import Response
from rest_framework.decorators import api_view
from watchlist.models import Movies
from .serializers import MovieSerializer


@api_view(http_method_names=['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movies.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = MovieSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(http_method_names=['GET', 'PUT'])
def movie_details(request, pk):
    if request.method == 'GET':
        try:
            movie = Movies.objects.get(pk=pk)
        except Movies.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=404)
    
        serializer = MovieSerializer(movie)  
        return Response(serializer.data)
    
    if request.method == 'PUT':
        movie = Movies.objects.get(pk=pk)
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)



