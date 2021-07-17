from django.db import models

# Create your models here.
class movieUpcoming(models.Model):
    rdate = models.DateField();
    name = models.CharField(max_length=25);
    actor = models.CharField(max_length=25);
    actress = models.CharField(max_length=25);
    rating = models.IntegerField();