from django.db import models

# Create your models here.
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    feedback = models.TextField()
    satisfaction = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name
    