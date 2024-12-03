from django.shortcuts import render, redirect, get_object_or_404
from .forms import TweetForm, UserForm, SearchForm
from .models import Tweet
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout

# Create your views here.
def home(request):
    return render(request, 'home.html')

def show_tweet(request):
    form = SearchForm() 
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets, 'form': form})

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('show_tweet')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('show_tweet')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user = request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('show_tweet')
    return render(request, 'tweet_delete.html', {'tweet': tweet})

def register_User(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')
    else:
        form = UserForm()
    return render(request, 'registration/register.html', {'form': form})


# Search
def search(request):
    form = SearchForm(request.GET or None)
    tweets = Tweet.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            keywords = query.split()
            for keyword in keywords:
                tweets = tweets.filter(text__icontains=keyword) | tweets.filter(user__username__icontains=keyword)
    return render(request, 'search_details.html', {'form': form, 'tweets': tweets})




