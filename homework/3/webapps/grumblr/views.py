from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

#Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

#Used to create and manually log in a user

from django.contrib.auth import login, authenticate


@login_required
def homepage(request):
	return render(request, 'grumblr/homepage.html', {})

def registration(request):
	context = {}

	if request.method == 'GET':
		return render(request, 'grumblr/registration.html', context)

	return redirect('/homepage.html')