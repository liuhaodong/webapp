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
	context['button_clicked'] = ''
	context['result'] = ''
	context['num_displayed']=''
	context['hidden_value']=''

	if 'button_clicked' in request.POST:

		context['button_clicked'] = request.POST['button_clicked']
		context['num_displayed'] = request.POST['num_displayed']
		context['hidden_value'] = request.POST['hidden_value']
		context['hidden_operator'] = request.POST['hidden_operator']
		context['hidden_lastbutton'] = request.POST['hidden_lastbutton']

		operand1 = context['hidden_value']
		operand2 = context['num_displayed']
		operator = context['hidden_operator']

		#A number is clicked
		if not isOperatorButton(context['button_clicked']):
			if isOperatorButton(context['hidden_lastbutton']):
				context['result'] = context['button_clicked']
				context['hidden_lastbutton'] = context['button_clicked']
			else:
				context['result'] = context['num_displayed'] + context['button_clicked']
				context['hidden_lastbutton'] = context['button_clicked']
		#An operator is clicked
		else:
			if context['button_clicked'] == 'c':
				context['result'] = ''
				context['hidden_value']=''
				context['hidden_lastbutton']=''
				context['hidden_operator'] =''
			else:
				context['result'] = calculate(operand1,operand2,operator)
				context['hidden_value'] = context['result']
				context['hidden_operator'] = context['button_clicked']
				context['hidden_lastbutton'] = context['button_clicked']
		

	else:
		operand1 = 0
		operand2 = 0
		operator = ''
	
	return render(request,'generic-calculator.html',context)


def isOperatorButton(post_parameters):
	button_clicked = ''
	operator_set = set()
	operator_set.add('+')
	operator_set.add('-')
	operator_set.add('*')
	operator_set.add('/')
	operator_set.add('c')
	operator_set.add('=')

	if post_parameters in operator_set:
			return True

	return False

def calculate(operand1, operand2, operator):
	if operator == '':
		return operand2
	elif operator == '+':
		return int(operand1)+int(operand2)
	elif operator == '-':
		return int(operand1)-int(operand2)
	elif operator == '*':
		return int(operand1)*int(operand2)
	elif operator == '/':
		return int(operand1)/int(operand2)
	elif operator == 'c':
		return ''
	elif operator == '=':
		return operand2
	else: 
		return ''
