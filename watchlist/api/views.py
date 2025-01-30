from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from watchlist.models import Movies
from .serializers import MovieSerializer


class MovieListApiView(APIView):

    def get(self, request):
        movies = Movies.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetailApiView(APIView):

    def get(self, request, pk):
        try:
            movie = Movies.objects.get(pk=pk)
        except Movies.DoesNotExist:
            return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        try:
            movie = Movies.objects.get(pk=pk)
        except Movies.DoesNotExist:
            return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            movie = Movies.objects.get(pk=pk)
        except Movies.DoesNotExist:
            return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

        movie.delete()
        return Response({'delete': "Movie has been deleted"}, status=status.HTTP_204_NO_CONTENT)
