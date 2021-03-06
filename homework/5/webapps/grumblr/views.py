from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core import serializers
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from django.db.models import Q
from django.http import HttpResponse, Http404

# Helper function to guess a MIME type from a file name
from mimetypes import guess_type

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail

from itertools import chain
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
from operator import itemgetter

from django.views.decorators.csrf import csrf_protect
import json
import json as simplejson

from grumblr.models import *
from grumblr.forms import *


@login_required
def homepage(request):
    tmp_following = Follow.objects.filter(
        following=request.user, follower=request.user)
    tmp_following.delete()
    posts = Post.objects.filter(user=request.user).order_by('-date')
    comments = Comment.objects.all()
    tmp_profile_set = Profile.objects.filter(user=request.user)
    if tmp_profile_set.count() == 0:
        return redirect('profile', id=request.user.id)
    else:
        pass
    profile = Profile.objects.get(user=request.user)
    post_contents = []
    for post in posts:
        content = {}
        content['dislike'] = False
        if DislikeGrumbl.objects.filter(user=request.user, post=post).count() > 0:
            content['dislike'] = True
        if PostPic.objects.filter(post=post).count() > 0:
            content['post_pic'] = True
        content['profile'] = Profile.objects.get(user=post.user)
        content['post'] = post
        content['comments'] = Comment.objects.filter(post=post)
        post_contents.append(content)

    recommends = []
    recommend_users = get_recommend_users(request)
    for user in recommend_users:
        recommend = {}
        recommend['recommend_user'] = user
        recommend['recommend_profile'] = Profile.objects.get(user=user)
        recommends.append(recommend)
    return render(request, 'grumblr/homepage.html', {'post_contents': post_contents, 'profile': profile, 'recommends': recommends})


@login_required
def get_recommend_users(request):
    context = {}
    follows = Follow.objects.filter(follower=request.user)
    followings_id = []
    followings_id.append(request.user.id)
    for follow in follows:
        followings_id.append(follow.following.id)
    recommend_users = User.objects.all().exclude(id__in=followings_id)
    return recommend_users


@login_required
def user_stream(request):
    follows = Follow.objects.filter(follower=request.user)
    following_posts = []
    for follow in follows:
        tmp_posts = Post.objects.all().order_by(
            '-date').filter(user=follow.following)
        following_posts = list(chain(following_posts, tmp_posts))
    following_posts = sorted(following_posts, key=lambda post: post.id, reverse=True)
    following_contents = []
    for post in following_posts:
        if BlockUser.objects.filter(blocked_user=request.user, blocking_user=post.user).count():
            continue
        content = {}
        content['dislike'] = False
        if DislikeGrumbl.objects.filter(user=request.user, post=post).count() > 0:
            content['dislike'] = True
        if PostPic.objects.filter(post=post).count() > 0:
            content['post_pic'] = True
        content['profile'] = Profile.objects.get(user=post.user)
        content['post'] = post
        content['comments'] = Comment.objects.filter(post=post)
        following_contents.append(content)
    recommends = []
    recommend_users = get_recommend_users(request)
    for user in recommend_users:
        recommend = {}
        recommend['recommend_user'] = user
        recommend['recommend_profile'] = Profile.objects.get(user=user)
        recommends.append(recommend)
    return render(request, 'grumblr/user_stream.html', {'following_contents': following_contents, 'recommends': recommends})


@login_required
def specified_user_stream(request, id):
    tmp_user = User.objects.get(id=id)
    posts = Post.objects.filter(user=tmp_user)
    following_contents = []
    for post in posts:
        if BlockUser.objects.filter(blocked_user=request.user, blocking_user=post.user).count():
            continue
        content = {}
        content['dislike'] = False
        if DislikeGrumbl.objects.filter(user=request.user, post=post).count() > 0:
            content['dislike'] = True
        if PostPic.objects.filter(post=post).count() > 0:
            content['post_pic'] = True
        content['profile'] = Profile.objects.get(user=post.user)
        content['post'] = post
        content['comments'] = Comment.objects.filter(post=post)
        following_contents.append(content)
    recommends = []
    recommend_users = get_recommend_users(request)
    for user in recommend_users:
        recommend = {}
        recommend['recommend_user'] = user
        recommend['recommend_profile'] = Profile.objects.get(user=user)
        recommends.append(recommend)
    specified_user = {}
    specified_user['user'] = tmp_user
    specified_user['is_user_page'] = True
    specified_user['following'] = (
        Follow.objects.filter(follower=request.user, following=tmp_user).count() > 0)
    specified_user['blocking'] = (BlockUser.objects.filter(
        blocking_user=request.user, blocked_user=tmp_user).count() > 0)
    return render(request, 'grumblr/user_stream.html', {'following_contents': following_contents, 'recommends': recommends, 'specified_user': specified_user})


@transaction.atomic
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

    if len(User.objects.filter(username=request.POST['username'])) > 0:
        errors.append('Username is already taken.')

    if errors:
        return render(request, 'grumblr/registration.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=request.POST['username'],
                                        password=request.POST['password'], email=request.POST['email'])
    new_user.is_active = False
    new_user.save()

    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(new_user)

    email_body = """
Welcome to the Grumblr.  Please click the link below to
verify your email address and complete the registration of your account:

  http://%s%s
""" % (request.get_host(),
       reverse('confirm', args=(new_user.username, token)))

    send_mail(subject="Verify your email address",
              message=email_body,
              from_email="haodongl@andrew.cmu.edu",
              recipient_list=[new_user.email])

    context['email'] = request.POST['email']

    # Logs in the new user and redirects to his/her todo list
   # new_user = authenticate(username=request.POST['username'], \
    #                        password=request.POST['password'])
   # login(request, new_user)
    return render(request, 'grumblr/needs_confirmation.html', context)


@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'grumblr/confirmed.html', {})


@login_required
@csrf_protect
def add_post(request):
    errors = []
    if not 'post' in request.POST or not request.POST['post']:
        errors.append('Post content cant be empty')
    else:
        new_post = Post(subject=request.POST['subject'], text=request.POST['post'], user=request.user)
        new_post.save()
        if 'post_picture' in request.FILES and request.FILES['post_picture']:
                new_post_pic = PostPic(post=new_post, post_picture=request.FILES['post_picture'])
                new_post_pic.save()

    posts = Post.objects.filter(user=request.user)
    context = {'posts' : posts, 'errors' : errors}
    return redirect('/homepage')

def get_post_picture(request, post_id):
    post_pic = get_object_or_404(PostPic, post=Post.objects.get(id=post_id))
    if not post_pic.post_picture:
        raise Http404
    content_type = guess_type(post_pic.post_picture.name)
    print(content_type)
    return HttpResponse(post_pic.post_picture, content_type=content_type)


@login_required
def add_comment(request):
    errors = []
    data = {}
    if request.method == 'POST':
        json_data = simplejson.loads(request.body)
        print(json_data)
    try:
        if not 'comment' in json_data or not json_data['comment']:
            errors.append('Comment content cant be empty')
        else:
            new_comment = Comment(content=json_data['comment'], post=Post.objects.get(id=json_data['post_id']), user=request.user)
            new_comment.save()
            data['post_id'] = new_comment.post.id
            data['comment_content'] = new_comment.content
            data['comment_id'] = new_comment.id
            data['comment_user_name'] = request.user.username
            data['comment_user_id'] = request.user.id
            return HttpResponse(json.dumps(data), content_type = "application/json")
    except KeyError:
        HttpResponseServerError("Malformed data!") 
    return HttpResponse(data, content_type='application/json')


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
    context = {'posts': posts, 'errors': errors}
    return redirect('/homepage')


@login_required
def block_user(request, id):
    errors = []
    if id == request.user.id:
        return
    try:
        tmp_blocked = User.objects.get(id=id)
        new_block = BlockUser(
            blocking_user=request.user, blocked_user=tmp_blocked)
    except ObjectDoesNotExist:
        errors.append('Block User Does Not Exist')
    new_block.save()
    return redirect('/user_stream_' + str(id))


@login_required
def unblock_user(request, id):
    errors = []
    try:
        block_to_delete = BlockUser.objects.get(
            blocked_user=User.objects.get(id=id), blocking_user=request.user)
        block_to_delete.delete()
    except ObjectDoesNotExist:
        errors.append('The block did not exist')
    return redirect('/user_stream_' + str(id))


@login_required
def dislike_post(request, id):
    tmp_dislike_set = DislikeGrumbl.objects.filter(
        user=request.user, post=Post.objects.get(id=id))
    if tmp_dislike_set.count() == 0:
        new_dislike = DislikeGrumbl(
            user=request.user, post=Post.objects.get(id=id))
        new_dislike.save()
    else:
        pass
    return redirect('/homepage')


@login_required
def delete_dislike(request, id):
    errors = []
    try:
        block_to_delete = DislikeGrumbl.objects.get(
            user=request.user, post=Post.objects.get(id=id))
        block_to_delete.delete()
    except ObjectDoesNotExist:
        errors.append('The dislike did not exist')
    return redirect('/homepage')


@login_required
def search_post(request):
    context = {}
    keyword = request.GET.get('keyword', False)
    posts = Post.objects.filter(
        Q(subject__icontains=keyword) | Q(text__icontains=keyword)).order_by('-date')
    search_contents = []
    for post in posts:
        if BlockUser.objects.filter(blocked_user=request.user, blocking_user=post.user).count():
            continue
        content = {}
        content['dislike'] = False
        if DislikeGrumbl.objects.filter(user=request.user, post=post).count() > 0:
            content['dislike'] = True
        content['profile'] = Profile.objects.get(user=post.user)
        content['post'] = post
        content['comments'] = Comment.objects.filter(post=post)
        search_contents.append(content)
    recommends = []
    recommend_users = get_recommend_users(request)
    for user in recommend_users:
        recommend = {}
        recommend['recommend_user'] = user
        recommend['recommend_profile'] = Profile.objects.get(user=user)
        recommends.append(recommend)
    context = {'following_contents': search_contents, 'recommends': recommends}
    return render(request, 'grumblr/user_stream.html', context)


@login_required
def profile(request, id):
    context = {}
    tmp_profile_set = Profile.objects.filter(user=request.user)
    if tmp_profile_set.count() == 0:
        new_profile = Profile(user=request.user)
        new_profile.save()
    else:
        pass
    showEditProfileButton = False
    if get_object_or_404(User, id=id) == request.user:
        showEditProfileButton = True
    user_profile = Profile.objects.get(user=User.objects.get(id=id))
    recommends = []
    recommend_users = get_recommend_users(request)
    for user in recommend_users:
        recommend = {}
        recommend['recommend_user'] = user
        recommend['recommend_profile'] = Profile.objects.get(user=user)
        recommends.append(recommend)
    context = {'profile': user_profile, 'recommends': recommends,
               'showEditProfileButton': showEditProfileButton}
    return render(request, 'grumblr/profile.html', context)


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
    tmp_following = User.objects.get(id=id)
    new_follow = Follow(follower=request.user, following=tmp_following)
    new_follow.save()
    return redirect('/user_stream_' + str(id))


@login_required
def unfollow(request, id):
    follow_to_delete = get_object_or_404(
        Follow, follower=request.user, following=User.objects.get(id=id))
    follow_to_delete.delete()
    return redirect('/user_stream_' + str(id))

@login_required
def check_update(request, post_id):
    follows = Follow.objects.filter(follower=request.user)
    following_posts = []
    for follow in follows:
        tmp_posts = Post.objects.all().filter(user=follow.following, id__gt=post_id)
        following_posts = list(chain(following_posts, tmp_posts))
    following_posts = sorted(following_posts, key=lambda post: post.id, reverse=False)
    following_contents = []
    for post in following_posts:
        if BlockUser.objects.filter(blocked_user=request.user, blocking_user=post.user).count():
            continue
        content = {}
        comments = []
        content['dislike'] = False
        if DislikeGrumbl.objects.filter(user=request.user, post=post).count() > 0:
            content['dislike'] = True
        if PostPic.objects.filter(post=post).count() > 0:
            content['post_pic'] = True
        profile = Profile.objects.get(user=post.user)

        content['post_id'] = post.id
        content['post_subject'] = post.subject
        content['post_text'] = post.text
        content['post_user_id'] = post.user.id
        content['profile_id'] = profile.id
        content['post_user_name'] = post.user.username
        tmp_comments = Comment.objects.filter(post=post)
        for comment in tmp_comments:
            tmp_comment = {}
            tmp_comment['comment_id'] = comment.id
            tmp_comment['comment_content'] = comment.content
            tmp_comment['comment_user_name'] = comment.user.username
            tmp_comment['comment_user_id'] = comment.user.id
            comments.append(tmp_comment)
        content['comments'] = comments
        following_contents.append(content) 
    return HttpResponse(json.dumps(following_contents), content_type = "application/json")


@login_required
def edit_profile(request):
    context = {}
    recommends = []
    recommend_users = get_recommend_users(request)
    for user in recommend_users:
        recommend = {}
        recommend['recommend_user'] = user
        recommend['recommend_profile'] = Profile.objects.get(user=user)
        recommends.append(recommend)
    if request.method == 'GET':
        context['recommends'] = recommends
        return render(request, 'grumblr/edit_profile.html', context)
    else:
        tmp_profile_set = Profile.objects.filter(user=request.user)
        if tmp_profile_set.count() == 0:
            new_profile = Profile(user=request.user)
            new_profile.save()
        else:
            pass
        user_profile = Profile.objects.get(user=request.user)
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

    context = {'profile': user_profile, 'recommends': recommends}
    return render(request, 'grumblr/profile.html', context)


def forgot_password(request):
    if request.method == 'POST':
        return password_reset(request, 
            from_email=request.POST.get('email'))
    else:
        return render(request, 'grumblr/forgot_password.html')



