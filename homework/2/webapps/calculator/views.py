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


def calculator(request):
	context = {};
	context['button_clicked'] = '';
	if 'button_clicked' in request.POST:
		context['button_clicked'] = request.POST['button_clicked']
	return render(request,'generic-calculator.html',context)