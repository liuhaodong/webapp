from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

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

from grumblr.models import *
from grumblr.forms import *

@login_required
def homepage(request):
    posts = Post.objects.filter(user=request.user) 
    comments = Comment.objects.all()
    profile = Profile.objects.get(user = request.user)
    return render(request, 'grumblr/homepage.html', {'posts' : posts, 'comments' : comments, 'profile' : profile})

@login_required
def user_stream(request):
    follows = Follow.objects.filter(follower = request.user)
    following_posts = []
    for follow in follows:
        tmp_posts = Post.objects.filter(user = follow.following)
        following_posts = list(chain(following_posts, tmp_posts))
    return render(request, 'grumblr/user_stream.html', {'posts' : following_posts})

@login_required
def specified_user_stream(request, id):
    tmp_user = User.objects.get(id=id)
    posts = Post.objects.filter(Q(user=tmp_user))
    return render(request, 'grumblr/user_stream.html', {'posts' : posts})


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
        new_comment = Comment(content=request.POST['comment'], post=Post.objects.get(id = request.POST['post_id']), user=User.objects.get(id = request.POST['user_id']))
        new_comment.save()
    return redirect('/homepage')

@login_required
def delete_post(request, id):
    errors = []

    try:
        post_to_delete = Post.objects.get(id=id, user=request.user)
        post_to_delete.delete()
    except ObjectDoesNotExist:
        errors.append('The post did not exist in your todo list.')

    posts = Post.objects.filter(user=request.user)
    context = {'posts' : posts, 'errors' : errors}
    return redirect('/homepage')


def search_post(request):
    context={}
    keyword = request.POST.get('keyword',False)
    print(keyword)
    posts = Post.objects.filter(Q(subject__icontains=keyword) | Q(text__icontains=keyword))
    context = {'posts' : posts}
    return render(request, 'grumblr/search_result.html',context)

@login_required
def profile(request):
    context={}
    tmp_profile_set = Profile.objects.filter(user = request.user)
    if tmp_profile_set.count() == 0:
        new_profile = Profile(user=request.user)
        new_profile.save()
    else:
        pass
    user_profile = Profile.objects.get(user = request.user)
    context = {'profile' : user_profile}
    return render(request,'grumblr/profile.html',context)


@login_required
def get_picture(request, id):
    profile = get_object_or_404(Profile, user=request.user, id=id)
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
    return redirect('/homepage');

@login_required
def edit_profile(request):
    context = {}
    if request.method == 'GET':
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
            print("pic inside")
            user_profile.id_picture = request.FILES['id_picture']
        print("after")
	user_profile.save()
        context = {'profile' : user_profile}
    return render(request,'grumblr/profile.html',context)
