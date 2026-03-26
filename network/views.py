import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import Http404, JsonResponse
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import InvalidPage, EmptyPage

from .models import User, Post
from .forms import PartialPostForm


def index(request):
    # Retrieve all posts from DB
    posts = Post.objects.all().order_by("-creation_date")
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page((request.GET.get("page")))
    elided_page_range = paginator.get_elided_page_range(page_obj.number)
    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "elided_page_range": elided_page_range
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    


@login_required
def new_post(request):
    if request.method == "GET":
        # Create empty post form
        form = PartialPostForm()
    else:
        post = Post(owner=request.user)
        form = PartialPostForm(request.POST, instance=post)
        # If data is valid:
        if form.is_valid():
            # Create post in db and redirect to all posts
            post = form.save()
            return HttpResponseRedirect(reverse("index"))
    
    # Render new-post route with form (either empty or filled with invalid data)
    return render(request, "network/new_post.html", {
        "form": form
    })



def profile(request, user_pk):
    try:
        profile_user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    if request.user in profile_user.followers.all():
        is_following = True
    else:
        is_following = False
    # Get profile's posts and paginate them
    posts = profile_user.posts.order_by("-creation_date")
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    elided_page_range = paginator.get_elided_page_range(page_obj.number)
    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "page_obj": page_obj,
        "elided_page_range": elided_page_range,
        "is_following": is_following
    })


@login_required
def follow(request, user_pk):
    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        raise Http404
    
    # Modify User's followers to include/exclude current user
    if request.user in user.followers.all():
        user.followers.remove(request.user)
    else:
        user.followers.add(request.user)
    return HttpResponseRedirect(reverse("profile", args=[user_pk]))

@login_required
def following(request):
    # Retrieve all posts from DB that belong to any profile that the user follows
    followers = request.user.following.all()
    posts = Post.objects.filter(owner__in=followers).order_by("-creation_date")
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page((request.GET.get("page")))
    elided_page_range = paginator.get_elided_page_range(page_obj.number)
    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "elided_page_range": elided_page_range,
        "following": True
    })




#### API Routes #####
@csrf_exempt
def post(request, post_pk):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthenticated User"})
    # Attempt to retrive post
    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"})
    # If method is not PUT, respond with error JSON message
    if request.method != "PUT":
        return JsonResponse({"error": "PUT method required"})
    
    
    data = json.loads(request.body)
    if data.get("like") is not None: # like/unlike the button and respond with a proper JSON message
        if data["like"] == True:
            post.liked_by.add(request.user)
            return JsonResponse({"message": "Liked Post", "likes": post.liked_by.count()})
        else:
            post.liked_by.remove(request.user)
            return JsonResponse({"message": "Disliked Post", "likes": post.liked_by.count()})
    
    if data.get("post-text") is not None: # like/unlike the button and respond with a proper JSON message
        if request.user != post.owner:
            return JsonResponse({"error": "Only post owners can edit their posts"})
        post.text = data["post-text"]
        post.save()
        return JsonResponse({"message": "Edited Post"})
    
    return JsonResponse({"error": "No action matches the request body"})