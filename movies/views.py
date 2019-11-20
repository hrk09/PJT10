from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Movie, Review, Genre
from .forms import ReviewForm
from  accounts.models import User


def index(request):
    movies = Movie.objects.all()
    context = { 'movies': movies }
    return render(request, 'movies/index.html', context)


@require_GET
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.reviews.all()
    form = ReviewForm()
    context = {
        'movie': movie,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'movies/detail.html', context)


@require_POST
def create_review(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie_id = movie_pk
            review.user = request.user
            review.save()
    return redirect('movies:detail', movie_pk)


@require_POST
def delete_review(request, movie_pk, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        movie = get_object_or_404(Movie, pk=movie_pk)
        if review.user == request.user or movie.user == request.user:   
            review.delete()
        return redirect('movies:detail', movie_pk)


@login_required
def like(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    # exists 한개의 데이터라도 존재하면 true
    if movie.liked_users.filter(pk=user.pk).exists():
    # if user in movie.liked_users.all():
        user.liked_movies.remove(movie)
        liked = False 
    else:
        user.liked_movies.add(movie)
        liked = True
    context = {
        'liked': liked, 
        'count': movie.liked_users.count()
    }
    return redirect('movies:detail', movie_pk)


@login_required
def follow(request, movie_pk, review_pk, user_pk):
    # 로그인한 유저가 게시글 유저를 Follow or unfollow 한다. 
    user = request.user
    person = get_object_or_404(User, pk=user_pk)

    if user in person.followers.all(): # 이미 팔로워다
        person.followers.remove(user) # 언팔 
    else:
        person.followers.add(user) # 팔로우함

    return redirect('movies:detail', movie_pk)

