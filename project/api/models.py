from django.db import models

# Create your models here.


class Student(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.id}-{self.first_name}"