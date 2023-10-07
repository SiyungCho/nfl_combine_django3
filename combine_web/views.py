from django.shortcuts import render
from .forms import input_data_Form
from .models import input_data
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def home(request):
    return render(request, 'combine_web/base.html')

def input(request):
    return render(request, 'combine_web/input.html', {'form':UserCreationForm()})