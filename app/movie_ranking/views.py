from django.shortcuts import render, get_object_or_404

from movie_ranking.models import Movie
from movie_ranking.models import MovieImage
from movie_ranking.models import PttMovie
from movie_ranking.models import CountGoodAndBad

# class MovieViewSet(viewsets.ModelViewSet):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer
#     permission_classes = (IsAuthenticated,)
#     parser_classes = (JSONParser,)


def home(request):
    all_rows = Movie.objects.all()

    movies = [
        all_rows.filter(title=item["title"]).last()
        for item in Movie.objects.values("title")
        .distinct()
        .order_by("rating")
        .reverse()
    ]

    context = {
        'movies': movies
    }
    return render(request, "movies/home.html", context)


def detail_view(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # comment = Movie.objects.get(pk=movie_pk)
    comments = PttMovie.objects.filter(key_word=movie)
    images = MovieImage.objects.filter(movie=movie)
    count_good_bad = CountGoodAndBad.objects.filter(movie=movie)

    context = {
        'movie': movie,
        'comments': comments,
        'images': images,
        'count_good_bad': count_good_bad,
    }

    return render(request, "movies/detail.html", context)