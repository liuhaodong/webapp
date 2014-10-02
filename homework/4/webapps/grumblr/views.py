from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
#Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

#Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from django.db.models import Q
from django.http import HttpResponse, Http404

# Helper function to guess a MIME type from a file name
from mimetypes import guess_type

from itertools import chain
from datetime import datetime

from grumblr.models import *
from grumblr.forms import *

@login_required
def homepage(request):
    tmp_following = Follow.objects.filter(following=request.user, follower=request.user)
    tmp_following.delete()
    posts = Post.objects.filter(user=request.user).order_by('-date')
    comments = Comment.objects.all()
    tmp_profile_set = Profile.objects.filter(user = request.user)
    if tmp_profile_set.count() == 0:
        return redirect('/profile')
    else:
        pass
    profile = Profile.objects.get(user = request.user)
    post_contents = []
    for post in posts:
        content = {}
        content['dislike'] = False
        if DislikeGrumbl.objects.filter(user=request.user, post=post).count()>0:
            content['dislike'] = True
        content['profile'] = Profile.objects.get(user = post.user)
        content['post'] = post
        content['comments'] = Comment.objects.filter(post = post)
        post_contents.append(content)

    recommends = []
    recommend_users = get_recommend_users(request)
    for user in recommend_users:
        recommend = {}
        recommend['recommend_user'] = user
        recommend['recommend_profile'] = Profile.objects.get(user = user)
        recommends.append(recommend)
    return render(request, 'grumblr/homepage.html', {'post_contents' : post_contents, 'profile' : profile, 'recommends' : recommends})

@login_required
def get_recommend_users(request):
    context = {}
    follows = Follow.objects.filter(follower = request.user)
    followings_id = []
    followings_id.append(request.user.id)
    for follow in follows:
        followings_id.append(follow.following.id)
    recommend_users = User.objects.all().exclude(id__in = followings_id)
    return recommend_users

@login_required
def user_stream(request):
    follows = Follow.objects.filter(follower = request.user)
    following_posts = []
    for follow in follows:
        tmp_posts = Post.objects.filter(user = follow.following).order_by('-date')
        following_posts = list(chain(following_posts, tmp_posts))
    following_contents = []
    for post in following_posts:
        if BlockUser.objects.filter(blocked_user=request.user, blocking_user=post.user).count():
            continue
        content = {}
        content['dislike'] = False
        if DislikeGrumbl.objects.filter(user=request.user, post=post).count()>0:
            content['dislike'] = True
        content['profile'] = Profile.objects.get(user = post.user)
        content['post'] = post
        content['comments'] = Comment.objects.filter(post = post)
        following_contents.append(content)
    recommends = []
    recommend_users = get_recommend_users(request)
    for user in recommend_users:
        recommend = {}
        recommend['recommend_user'] = user
        recommend['recommend_profile'] = Profile.objects.get(user = user)
        recommends.append(recommend)
    return render(request, 'grumblr/user_stream.html', {'following_contents' : following_contents, 'recommends': recommends})

@login_required
def specified_user_stream(request, id):
    tmp_user = User.objects.get(id=id)
    posts = Post.objects.filter(Q(user=tmp_user))
    following_contents = []
    for post in posts:
        if BlockUser.objects.filter(blocked_user=request.user, blocking_user=post.user).count():
            continue
        content = {}
        content['dislike'] = False
        if DislikeGrumbl.objects.filter(user=request.user, post=post).count()>0:
            content['dislike'] = True
        content['profile'] = Profile.objects.get(user = post.user)
        content['post'] = post
        content['comments'] = Comment.objects.filter(post = post)
        following_contents.append(content)
    recommends = []
    recommend_users = get_recommend_users(request)
    for user in recommend_users:
        recommend = {}
        recommend['recommend_user'] = user
        recommend['recommend_profile'] = Profile.objects.get(user = user)
        recommends.append(recommend)
    specified_user = {}
    specified_user['user'] = tmp_user
    specified_user['following'] = (Follow.objects.filter(follower=request.user, following=tmp_user).count() > 0)
    specified_user['blocking'] = (BlockUser.objects.filter(blocking_user=request.user, blocked_user=tmp_user).count() > 0)
    return render(request, 'grumblr/user_stream.html', {'following_contents' : following_contents, 'recommends': recommends, 'specified_user': specified_user})

def registration(request):
    context = {}

    if request.method == 'GET':
        return render(request, 'grumblr/registration.html', context)

    errors = []
    context['errors'] = errors

	# Checks the validity of the form data
    if not 'username' in request.POST or not request.POST['username']:
        errors.append('Username is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
        context['username'] = request.POST['username']


    if len(User.objects.filter(username = request.POST['username'])) > 0:
        errors.append('Username is already taken.')

    if errors:
        return render(request, 'grumblr/registration.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=request.POST['username'], \
                                        password=request.POST['password'])

    new_user.save()

    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=request.POST['username'], \
                            password=request.POST['password'])
    login(request, new_user)
    return redirect('/homepage')

@login_required
def add_post(request):
    errors = []
    if not 'post' in request.POST or not request.POST['post']:
        errors.append('Post content cant be empty')
    else:
        new_post = Post(subject=request.POST['subject'], text=request.POST['post'], user=request.user)
        new_post.save()

    posts = Post.objects.filter(user=request.user)
    context = {'posts' : posts, 'errors' : errors}
    return redirect('/homepage')


@login_required
def add_comment(request):
    errors = []
    if not 'comment' in request.POST or not request.POST['comment']:
        errors.append('Comment content cant be empty')
    else:
        new_comment = Comment(content=request.POST['comment'], post=Post.objects.get(id = request.POST['post_id']), user=request.user)
        new_comment.save()
    return HttpResponseRedirect('/homepage')

@login_required
def delete_comment(request, id):
    errors = []
    try:
        comment_to_delete = Comment.objects.get(id=id, user=request.user)
        comment_to_delete.delete()
    except ObjectDoesNotExist:
        errors.append('The post did not exist in your todo list.')
    return redirect('/homepage')

@login_required
def delete_post(request, id):
    errors = []
    try:
        post_to_delete = Post.objects.get(id=id, user=request.user)
        post_to_delete.delete()
    except ObjectDoesNotExist:
        errors.append('The post did not exist.')

    posts = Post.objects.filter(user=request.user)
    context = {'posts' : posts, 'errors' : errors}
    return redirect('/homepage')

@login_required
def block_user(request, id):
    errors = []
    if id == request.user.id:
        return
    try:
        tmp_blocked = User.objects.get(id = id)
        new_block = BlockUser(blocking_user=request.user, blocked_user = tmp_blocked)
    except ObjectDoesNotExist:
        errors.append('Block User Does Not Exist')
    new_block.save()
    return redirect('/user_stream_'+str(id))

@login_required
def unblock_user(request, id):
    errors = []
    try:
        block_to_delete = BlockUser.objects.get(blocked_user=User.objects.get(id=id), blocking_user=request.user)
        block_to_delete.delete()
    except ObjectDoesNotExist:
        errors.append('The block did not exist')
    return redirect('/homepage')

@login_required
def dislike_post(request, id):
    tmp_dislike_set = DislikeGrumbl.objects.filter(user = request.user, post = Post.objects.get(id=id))
    if tmp_dislike_set.count() == 0:
        new_dislike = DislikeGrumbl(user = request.user, post = Post.objects.get(id=id))
        new_dislike.save()
    else:
        pass
    return redirect('/homepage')

@login_required
def delete_dislike(request, id):
    errors = []
    try:
        block_to_delete = DislikeGrumbl.objects.get(user=request.user, post = Post.objects.get(id=id))
        block_to_delete.delete()
    except ObjectDoesNotExist:
        errors.append('The dislike did not exist')
    return redirect('/homepage')

@login_required
def search_post(request):
    context={}
    keyword = request.POST.get('keyword',False)
    posts = Post.objects.filter(Q(subject__icontains=keyword) | Q(text__icontains=keyword))
    search_contents = []
    for post in posts:
        if BlockUser.objects.filter(blocked_user=request.user, blocking_user=post.user).count():
            continue
        content = {}
        content['dislike'] = False
        if DislikeGrumbl.objects.filter(user=request.user, post=post).count()>0:
            content['dislike'] = True
        content['profile'] = Profile.objects.get(user = post.user)
        content['post'] = post
        content['comments'] = Comment.objects.filter(post = post)
        search_contents.append(content)
    recommends = []
    recommend_users = get_recommend_users(request)
    for user in recommend_users:
        recommend = {}
        recommend['recommend_user'] = user
        recommend['recommend_profile'] = Profile.objects.get(user = user)
        recommends.append(recommend)
    context = {'following_contents' : search_contents, 'recommends': recommends}
    return render(request, 'grumblr/user_stream.html',context)

def profile(request):
    context={}
    tmp_profile_set = Profile.objects.filter(user = request.user)
    if tmp_profile_set.count() == 0:
        new_profile = Profile(user=request.user)
        new_profile.save()
    else:
        pass
    user_profile = Profile.objects.get(user = request.user)
    recommends = []
    recommend_users = get_recommend_users(request)
    for user in recommend_users:
        recommend = {}
        recommend['recommend_user'] = user
        recommend['recommend_profile'] = Profile.objects.get(user = user)
        recommends.append(recommend)
    context = {'profile' : user_profile, 'recommends': recommends}
    return render(request,'grumblr/profile.html',context)


def get_picture(request, id):
    profile = get_object_or_404(Profile, id=id)
    if not profile.id_picture:
        raise Http404

    content_type = guess_type(profile.id_picture.name)
    return HttpResponse(profile.id_picture, content_type=content_type)

@login_required
def follow(request, id):
    if id == request.user.id:
        return
    tmp_following = User.objects.get(id = id)
    new_follow = Follow(follower=request.user, following = tmp_following)
    new_follow.save()
    return redirect('/user_stream_'+str(id))

@login_required
def unfollow(request, id):
   follow_to_delete = get_object_or_404(Follow, follower=request.user, following=User.objects.get(id=id)) 
   follow_to_delete.delete()
   return redirect('/user_stream_'+str(id))

@login_required
def edit_profile(request):
    context = {}
    recommends = []
    recommend_users = get_recommend_users(request)
    for user in recommend_users:
        recommend = {}
        recommend['recommend_user'] = user
        recommend['recommend_profile'] = Profile.objects.get(user = user)
        recommends.append(recommend)
    if request.method == 'GET':
        context['recommends'] = recommends
        return render(request,'grumblr/edit_profile.html',context)
    else:
        tmp_profile_set = Profile.objects.filter(user = request.user)
        if tmp_profile_set.count() == 0 :
            new_profile = Profile(user=request.user)
            new_profile.save()
        else:
            pass
        user_profile = Profile.objects.get(user = request.user)
        if 'email' in request.POST and request.POST['email']:
            user_profile.email = request.POST['email']
        if 'motto' in request.POST and request.POST['motto']:
            user_profile.motto = request.POST['motto']
        if 'age' in request.POST and request.POST['age']:
            user_profile.age = request.POST['age']
        if 'fullname' in request.POST and request.POST['fullname']:
            user_profile.fullname = request.POST['fullname']
        if 'company' in request.POST and request.POST['company']:
            user_profile.company = request.POST['company']
        if 'address' in request.POST and request.POST['address']:
            user_profile.address = request.POST['address']
        if 'phone' in request.POST and request.POST['phone']:
            user_profile.phone = request.POST['phone']
        if 'language' in request.POST and request.POST['language']:
            user_profile.language = request.POST['language']
        if 'id_picture' in request.FILES and request.FILES['id_picture']:
            user_profile.id_picture = request.FILES['id_picture']
	user_profile.save()
    
    context = {'profile' : user_profile,'recommends' : recommends}
    return render(request,'grumblr/profile.html',context)
