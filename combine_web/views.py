from django.shortcuts import render, redirect
from .forms import input_data_Form
from .models import input_data
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def home(request):
    return render(request, 'combine_web/base.html')

def input(request):
    if(request.method=='GET'):
        return render(request, 'combine_web/input.html', {'form':UserCreationForm()})
    else:
        try:
            form = input_data_Form(request.POST)
            new_player = form.save(commit=False)#don't put in database just yet
            new_player.save()
            return render(request, 'combine_web/output.html', {'name':new_player.name})
        except ValueError:
            return render(request, 'combine_web/input.html', {'form':input_data_Form(), 'error':'Error occured in data passed'})
        
def output(request):
    return render(request, 'combine_web/output.html')