from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission

# Create your models here.

# Custom User Model to differentiate Employers & Job Seekers
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    
    # Fix conflicts by adding unique related names
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)


# Job Model
class Job(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'employer'})
    company_name = models.CharField(max_length=255,blank=True,null=True)  # Added company name
    company_website = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.TextField(blank=True,null=True)
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company_name}"
    

# Application Model
class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'job_seeker'})
    applicant_fullname = models.CharField(max_length=255 , blank=True,null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    skills = models.TextField(blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    cover_letter = models.FileField(upload_to='cover_letters/', blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.applicant_name} applied for {self.job.title}"
