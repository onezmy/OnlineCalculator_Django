from inspect import stack
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def calculator_action(request): 
    if request.method == 'GET':
        context = initial_context()
        return render(request, 'calculator.html', context)
    try:
        if request.POST['stack'] != request.POST['pre_stack'] or request.POST['entering'] != request.POST['pre_entering']:
            raise Exception("Changed")
        inputs = process_parameters(request)
        if 'button' in inputs:
            context = process_digit(inputs)
        else:
            context = process_operation(inputs)
        context['pre_stack'] = context['stack']
        context['pre_entering'] = context['entering']
        return render(request, 'calculator.html', context)
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})

def initial_context():
    context = {}
    context['output'] = 0
    context['stack'] = 0
    context['entering'] = True
    context['pre_stack'] = 0
    context['pre_entering'] = True
    return context

def process_parameters(request):
    if request.POST['button'] in "0123456789":
        return {'button': request.POST['button'], 'entering':request.POST['entering'], 'stack':request.POST['stack']}
    return {'operator':request.POST['button'], 'entering':request.POST['entering'], 'stack':request.POST['stack']}

def process_digit(inputs):
    stack_str = inputs['stack']
    stack_str = stack_str.split(',')
    if inputs['entering'] == 'True':
        stack_str[-1] = str(int(stack_str[-1])*10 + int(inputs['button']))
        ans = stack_str[-1]
    else:
        ans = str(inputs['button'])
        stack_str.append(ans)
        
    inputs['entering'] = 'True'
    inputs['output'] = ans
    inputs['stack'] = ','.join(stack_str)
    return inputs


def process_operation(inputs):
    stack_str = inputs['stack']
    stack_str = stack_str.split(',')
    if inputs['operator'] == 'push':
        if len(stack_str) < 3:
            inputs['stack'] += ',' + '0'
            inputs['output'] = '0'
            inputs['entering'] = 'True'
            
        else:
            inputs = initial_context() 
            raise Exception("Stack Overflow")
        return inputs
    
    else:
        if len(stack_str) <= 1:
            inputs = initial_context() 
            raise Exception("Stack Underflow")
        inputs['entering'] = False
        s1 = stack_str.pop()
        s2 = stack_str.pop()
        
        if inputs['operator'] == 'plus':
            ans = str(int(s1) + int(s2))

        elif inputs['operator'] == 'minus':
            ans = str(int(s2) - int(s1))

        elif inputs['operator'] == 'times':
            ans = str(int(s1) * int(s2))

        elif inputs['operator'] == 'divide':
            if int(s1) == 0:
                inputs = initial_context() 
                raise Exception("divide by 0")
            else:
                ans = str(int(int(s2) / int(s1)))   

        if len(stack_str) == 1:
            inputs['stack'] = stack_str[0] + ',' + ans
        else:
            inputs['stack'] = ans 

        inputs['output'] = ans
        return inputs





