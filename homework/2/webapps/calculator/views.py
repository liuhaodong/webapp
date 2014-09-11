from django.shortcuts import render

# Create your views here.
def hello_world(request):
	return render(request, 'generic-hello.html',{})

def hello(request):
	context = {};
	context['person_name'] = ''

	if 'username' in request.GET:
		context['person_name'] = request.GET['username']

	return render(request,'greet.html',context)
