from django import forms
from .models import Application,Job,JobCategory,Interview
from django.contrib.auth.models import User

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ['job', 'job_seeker', 'status']


class JobForm(forms.ModelForm):

    new_job_category = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter new category'}),
    )


    application_deadline = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Job
        exclude = ['employer']
        widgets = {
            'job_category': forms.Select(attrs={'class': 'form-control'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'application_deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
       
    def clean(self):
        cleaned_data = super().clean()
        new_category = cleaned_data.get("new_job_category")

        if new_category:
            category, created = JobCategory.objects.get_or_create(name=new_category)
            cleaned_data["job_category"] = category

        return cleaned_data
    

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    user_role = forms.ChoiceField(choices=[('employer', 'Employer'), ('job_seeker', 'Job Seeker')], widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match!")

        return cleaned_data    


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['interview_date', 'venue']

