from django.forms import ModelForm
from .models import input_data

class ToDo_Form(ModelForm):
    class Meta:
        model = input_data
        fields = ['name',"player_POS", "player_Height", "player_Weight", "player_40Yard", "player_BenchPress", "player_Vert", "player_Broad", "player_Shuttle", "player_3Cone"]