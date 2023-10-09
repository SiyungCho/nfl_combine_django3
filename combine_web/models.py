from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
class input_data(models.Model):
    name = models.CharField(max_length = 100)
    player_POS = models.CharField(max_length=2)  # Assuming positions are represented as two-letter codes like 'CB'
    player_Height = models.DecimalField(max_digits=4, decimal_places=2)  # Height in inches
    player_Weight = models.PositiveIntegerField()  # Weight in pounds
    player_40Yard = models.DecimalField(max_digits=4, decimal_places=2)  # 40-yard dash time in seconds
    player_BenchPress = models.PositiveIntegerField()  # Bench press reps
    player_Vert = models.DecimalField(max_digits=4, decimal_places=1)  # Vertical jump in inches
    player_Broad = models.PositiveIntegerField()  # Broad jump in inches
    player_Shuttle = models.DecimalField(max_digits=4, decimal_places=2)  # Shuttle run time in seconds
    player_3Cone = models.DecimalField(max_digits=4, decimal_places=2)  # 3-cone drill time in seconds
    prediction_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.00), MaxValueValidator(1.00)])

    def __str__(self):
        return self.name