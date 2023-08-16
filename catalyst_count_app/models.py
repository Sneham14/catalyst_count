from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator, MinLengthValidator
from django.contrib.auth.models import AbstractUser
import os
from chunked_upload.models import ChunkedUpload


MyChunkedUpload = ChunkedUpload

def upload_path(instance, filename):
    return os.path.join('catalyst_count', 'uploads', filename)

class CompanyDataModel(models.Model):
    
    name = models.CharField(max_length=120)
    domain = models.URLField(max_length=200)
    year_founded = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        null=True,  # Allow null values
        blank=True,  # Allow empty input
    )
    industry = models.CharField(max_length=120, null=True,  blank=True)
    size_range =  models.CharField(
        max_length=20,  # Adjust max_length as needed
        validators=[
            RegexValidator(r'^\d+\+?$'),        # For formats like "10000+"
            RegexValidator(r'^\d+-\d+$'),       # For formats like "51-200"
            RegexValidator(r'^[A-Za-z]+-\d+$'), # For formats like "Nov-50"
        ], 
    )
    locality = models.TextField(null=True,  blank=True)
    country = models.CharField(max_length=120, null=True,  blank=True)
    linkedin_url = models.URLField(null=True,  blank=True)
    current_employee_estimate = models.BigIntegerField(  # Used BigIntegerField for larger values
        validators=[MinValueValidator(0)]
    )
    total_employee_estimate = models.BigIntegerField(# Used BigIntegerField for larger values
        validators=[MinValueValidator(0)]
    )
    uploaded_file = models.FileField(upload_to=upload_path, null=True, blank=True)


    def __str__(self):
        return self.name
    
class UserModel(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=120, unique=True)
    password = models.CharField(max_length=120, validators=[MinLengthValidator(8)])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
