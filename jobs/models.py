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

# job category
class JobCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

# Job Type Model
class JobType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# Job Model
class Job(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'employer'})
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    job_title = models.CharField(max_length=200,null=True,blank=True)  
    description = models.TextField()
    required_skills = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100)
    salary_range = models.CharField(max_length=100,null=True,blank=True)  
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, blank=True)
    job_type = models.ForeignKey(JobType, on_delete=models.SET_NULL, null=True, blank=True)
    minimum_qualification = models.CharField(max_length=100, default="Bachelor")
    experience_level = models.CharField(max_length=100,default="Fresher")  
    application_deadline = models.DateField(null=True,blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.job_title} at {self.company_name}"
    

# Application Model
class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    ]
        
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'job_seeker'})
    applicant_fullname = models.CharField(max_length=255 , blank=True,null=True)
    qualification = models.CharField(max_length=100, default="Bachelor")
    experience = models.TextField(default="Fresher")
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    skills = models.TextField(blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    cover_letter = models.FileField(upload_to='cover_letters/', blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"{self.applicant_fullname} applied for {self.job.job_title}"
    

class Interview(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]
    application = models.OneToOneField('Application', on_delete=models.CASCADE)  # Link to application
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE)  # Employer conducting the interview
    interview_date = models.DateTimeField(null=True,blank=True)  # Date and time of interview
    venue = models.CharField(max_length=255)  # Interview venue
    status = models.CharField(max_length=20, choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed')], default='Scheduled')
    invitation_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    rejection_reason = models.TextField(blank=True, null=True)  # Store rejection reason
    
    def __str__(self):
        return f"Interview for {self.application.job_seeker} - {self.application.job.job_title}"    
