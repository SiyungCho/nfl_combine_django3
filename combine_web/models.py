from django.db import models

# Create your models here.
class input_data(models.Model):

    def __str__(self):
        return self.name