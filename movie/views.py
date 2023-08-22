from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Movie, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    name = request.GET.get('SearchMovie')
    movies = Movie.objects.all()
    count = movies.count
    if(movies.filter(title=name)):
      return render(request, 'home.html', {'count':count, 'movies': movies.filter(title=name), 'searchTerm': name})  
    return render(request, 'home.html', {'count':count, 'movies': movies})

def about(request):
    return HttpResponse('<h1>Page About</h1>')

def movie(request):
   # name = request.GET.get('SearchMovie')
   # movie = Movie.objects.filter(title = name)   
    return render(request, 'movie.html')

def detail(request, movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    reviews = Review.objects.filter(movie=movie)
    return render(request, 'detail.html', {'movie':movie, 'reviews': reviews})

@login_required
def createreview(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'GET':
        return render(request, 'createreview.html', {'form': ReviewForm(), 'movie':movie})
    else:
        try:
            form = ReviewForm(request.POST)
            newreview = form.save(commit=False)
            newreview.user = request.user
            newreview.movie = movie
            newreview.save()
            return redirect('detail', newreview.movie.id)
        except ValueError:
            return render(request, 'createreview.html', {'form':ReviewForm(), 'error':'bad data passed in'})

@login_required        
def updatereview(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    if request.method == 'GET':
        form = ReviewForm(instance=review)
        return render(request, 'updatereview.html', {'review': review, 'form':form})
    else:
        try:
            form = ReviewForm(request.POST, instance = review)
            form.save()
            return redirect('detail', review_id)
        except ValueError:
            return render(request, "updatereview.html")

@login_required
def deletereview(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    review.delete()
    return redirect("detail", review.movie.id)
