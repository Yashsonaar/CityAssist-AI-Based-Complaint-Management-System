from django.db import models

class Complaint(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField()
    desc=models.TextField()
    
    def __str__(self):
        return self.name

