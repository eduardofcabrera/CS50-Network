from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from .models import User, Post, Like, Following


def index(request, start=0, end=10, mode='loadIndex'):

    if request.method == 'GET' or mode == 'loadPosts':

        posts_info = getPostsInfo(request, start, end)
        loadPlus = getLoadPlus(end)
        loadMinus = getLoadMinus(start)
        start+= 10
            
        return render(request, "network/index.html", {
            'posts_info': posts_info,
            'start': start,
            'loadPlus': loadPlus,
            'loadMinus': loadMinus
        })
    
    content = request.POST.get('textarea')
    user = request.user
    createPost(content, user)
    
    return HttpResponseRedirect(reverse("index"))

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

def getUserPage(request, user_id, start=0, end=10):
    
    user = getUser(request)
    user_page = getUserOfPage(user_id)
    i_follow = getIFollow(user, user_page)
    following = getFollowing(user_page)
    followers = getFollowers(user_page)
    posts = getPosts(request, user_page, start, end)
    my_page = getMyPage(user_page, user)
    number_of_following = getNumberFollowing(following)
    number_of_followers = getNumberFollowers(followers)
    loadPlus = getLoadPlusForUser(end, user_page)
    loadMinus = getLoadMinus(start)
    start += 10

    return render(request, "network/userPage.html", {
        "user_page": user_page,
        "posts": posts,
        "following": following,
        "followers": followers,
        "number_of_following": number_of_following, 
        "number_of_followers": number_of_followers,
        "i_follow": i_follow,
        "my_page": my_page,
        "loadPlus": loadPlus,
        "loadMinus": loadMinus,
        "start": start
    })

def getUser(request):
    user = request.user
    return user

def getUserOfPage(user_id):
    user_page = User.objects.get(pk=user_id)
    return user_page

def getIFollow(user, user_page):
    user_following = Following.objects.filter(user=user_page, following=user).first()
    if user_following == None:
        return False
    else:
        return True

def getFollowing(user_page):
    following = Following.objects.filter(following=user_page)
    return following

def getFollowers(user_page):
    followers = Following.objects.filter(user=user_page)
    return followers

def getMyPage(user_page, user):
    if user_page == user:
        return True
    return False

def getPosts(request, user_page, start, end):
    posts = Post.objects.filter(owner=user_page).order_by('pk').reverse()[start:end]
    posts = checkPosts(request, posts)
    return posts

def getNumberFollowing(following):
    return len(following)

def getNumberFollowers(followers):
    return len(followers)

def getLoadPlusForUser(end, user_page):
    numberOfPosts = len(Post.objects.filter(owner=user_page))
    if numberOfPosts - end >= 10:
        return True
    return False   

def getPostsInfo(request, start, end):

    posts = Post.objects.order_by('pk').reverse()[start:end]
    posts_info = checkPosts(request, posts)
    return posts_info

def checkPosts(request, posts):
    posts_info = getInfo_of_posts(request, posts) 
    return posts_info

def getInfo_of_posts(request, posts):

    posts_info = []
    user = request.user
    for post in posts:
        post_line = getPostLine(user, post)
        posts_info.append(post_line)

    return posts_info

def getPostLine(user, post):

    post_line = {}

    is_liked = getIsLiked(user, post)
    owner = getOwner(post)
    is_owner = getIsOwner(owner, user)
    numberOfLikes = getNumberOfLikes(post)

    post_line['post'] = post
    post_line['owner']= owner
    post_line['is_liked'] =  is_liked
    post_line['number_of_likes'] = numberOfLikes
    post_line['is_owner'] = is_owner

    return post_line

def getIsLiked(user, post):
    if(user.is_anonymous):
        return False
    else:
        likes = Like.objects.filter(owner=user, Post=post)
        if(len(likes) > 0):
            return True    

def getIsOwner(owner, user):
    if owner == user:
        return True
    return False

def getOwner(post):
    owner = User.objects.filter(posts_owner=post).first()
    return owner

def getNumberOfLikes(post):
    numberOfLikes = len(Like.objects.filter(Post=post))
    return numberOfLikes

def followingPage(request, start=0, end=10):
    
    user = getUser(request)
    following = getFollowing(user)
    users_followings = getUsersFollowings(following)
    all_posts = getAllPosts(request)
    posts = getPostsOfFollowing(users_followings, all_posts)
    loadPlus = getLoadPlusForFollowing(end, posts)
    loadMinus = getLoadMinus(start)
    posts = posts[start:end]
    posts_info = checkPosts(request, posts)
    start += 10


    return render(request, 'network/followingPage.html', {
        "posts_info": posts_info,
        "start": start,
        "loadPlus": loadPlus,
        "loadMinus": loadMinus 
    })

def getLoadPlusForFollowing(end, posts):
    numberOfPosts = len(posts)
    if(numberOfPosts - end >= 10):
        return True
    return False

def getUsersFollowings(following):
    users_following = []
    for user_follow in following:
        user = user_follow.user
        users_following.append(user)
    return users_following

def getPostsOfFollowing(users_followings, all_posts):
    
    posts_of_following = []
    for post in all_posts:
        owner = getOwner(post)
        if owner in users_followings:
            posts_of_following.append(post)
    return(posts_of_following)
    
def getAllPosts(request):
    posts = Post.objects.all().order_by("pk").reverse()
    return posts

def getPostsByUser(user):
    posts = Post.objects.filter(owner=user)
    return posts

@csrf_exempt
def show10Posts(request, mode, where, user_id):

    start = getStart(request)
    if request.method == 'POST' and mode == 'down':
        start -= 20
    end = getEnd(start)
    return chooseWhere(request, start, end, where, user_id)  


def chooseWhere(request, start, end, where, user_id):

    if where=='index' and user_id==0:
        return index(request, start, end, 'loadPosts')
    elif where=='userPage':
        return getUserPage(request, user_id, start, end)
    else:
        return followingPage(request, start, end)

def getStart(request):
    start = int(request.POST.get('start'))
    return start

def getEnd(start):
    start += 10
    return start

def getLoadMinus(start):
    if(start>=10):
        return True
    return False

def getLoadPlus(end):

    numberOfPosts = len(Post.objects.order_by('pk').reverse())
    if numberOfPosts - end >= 10:
        return True
    return False   

def createPost(content, user):

    new_post = Post.objects.create(post_content=content)
    user.posts_owner.add(new_post)

@csrf_exempt
def makeLike(request):
    
    if request.method == 'PUT':
        
        user = request.user
        data = json.loads(request.body)
        post_id = data['post_id']
        is_like = data['is_like']

        if(is_like):
            like(user, post_id)
        else:
            dislike(user, post_id)
        
    return HttpResponse(status=204)

def like(user, post_id):

    post = Post.objects.get(pk=post_id)
    likes = Like.objects.filter(owner=user, Post=post)
    if(len(likes) > 0):
        return None

    new_like = Like.objects.create()
    user.likes_owner.add(new_like)
    post.post_likes.add(new_like)


def dislike(user, post_id):
    
    post = Post.objects.filter(pk=post_id).first()
    likes = Like.objects.filter(owner=user, Post=post)
    for like in likes:
        like.delete()


@csrf_exempt
def changeFollow(request, user_page):
    
    if request.method == 'PUT':
        
        user = request.user
        data = json.loads(request.body)

        if data['mode'] == 'follow':
            follow(user, user_page)
        elif data['mode'] == 'unfollow':
            unfollow(user, user_page)
        else:
            return HttpResponse('ERROR')

    return HttpResponse('ERROR')

def follow(user, user_page):
    
    user_page = User.objects.get(username=user_page)
    new_following = Following.objects.create(user=user_page, following=user)
    new_following.save()

def unfollow(user, user_page):

    user_page = User.objects.get(username=user_page)
    following_user = Following.objects.filter(user=user_page, following=user).first()
    following_user.delete()


@csrf_exempt   
def editPost(request, post_id):
    
    if request.method == 'PUT':

        data = json.loads(request.body)
        content = data['content']

        post = Post.objects.get(pk=post_id)
        post.post_content = content
        post.save()

    return HttpResponse(status=204)


