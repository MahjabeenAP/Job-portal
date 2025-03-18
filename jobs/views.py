from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from .models import Job,Application,JobType,JobCategory,Interview
from .forms import ApplicationForm,JobForm,JobCategory,RegistrationForm,InterviewForm
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
# registration
User = get_user_model() 
def registerfn(request):
    if request.method == 'POST':
        u = request.POST.get('uname')
        e = request.POST.get('email')
        f = request.POST.get('fname')
        l = request.POST.get('lname')
        p1 = request.POST.get('psw1')
        p2 = request.POST.get('psw2')
        user_type = request.POST.get('user_type')  # Get user type from form

        if p1 == p2:
            if User.objects.filter(username=u).exists():
                return render(request, 'register.html', {'er': 'User already exists'})
            else:
                user = User.objects.create_user(username=u, first_name=f, last_name=l, email=e, password=p1, user_type=user_type)
                return redirect('/')
        else:
            return render(request, 'register.html', {'er': 'Passwords do not match'})

    return render(request, 'register.html')


# login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")

            # Redirect based on user role
            if hasattr(user, 'user_type'):
                if user.user_type == 'employer':
                    return redirect('/emp/')
                elif user.user_type == 'job_seeker':
                    return redirect('/alljobs/')
            else:
                return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

def logoutfn(request):
    auth.logout(request)
    return redirect('/') 

### my views   employer dashbord

def employer_dashboard(request):
    # Fetch all job categories and job types from the database
    job_categories = JobCategory.objects.all()
    job_types = JobType.objects.all()
    return render(request, 'empdash.html', {'job_categories': job_categories, 'job_types': job_types})


    # Handle adding a new job category
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        if category_name:
            JobCategory.objects.create(name=category_name)
            messages.success(request, 'Job category added successfully!')
        else:
            messages.error(request, 'Please enter a valid category name.')
    return redirect('/emp/')
    

   
    # Handle adding a new job type
def add_job_type(request):
    if request.method == 'POST':
        job_type_name = request.POST.get('job_type_name')
        if job_type_name:
            JobType.objects.create(name=job_type_name)
            messages.success(request, 'Job type added successfully!')
        else:
            messages.error(request, 'Please enter a valid job type name.')
    return redirect('/emp/')    


# post a job
@login_required
def job_create(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user  # Assuming the logged-in user is the employer
            job.save()
            print("job post success")
            messages.success(request, "Job posted successfully!")
            return redirect("/myjobs")  # Redirect to job listing page
        else:
            messages.error(request, "Please fill in all required fields.")
    else:
        form = JobForm()
    
    return render(request, "job_create.html", {"form": form, "page_title": "Create Job"})


#filter jobs
def my_jobs(request):
    jobs = Job.objects.filter(employer=request.user)
    return render(request, 'my_jobs.html', {'jobs': jobs})


def update_job(request,p_id):
    if request.method=='POST':
        x=Job.objects.get(id=p_id)
        form=JobForm(request.POST,request.FILES,instance=x)
        if form.is_valid():
            form.save()
            return redirect('/myjobs/')
    else:
        x=Job.objects.get(id=p_id)
        form=JobForm(instance=x)
        return render(request, "job_create.html", {"form": form, "page_title": "Edit Job"})

    

# delete job    
def delete_job(request,p_id):
    job = get_object_or_404(Job, id=p_id, employer=request.user)  # Ensure only the job owner can delete

    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted successfully!")
        return redirect('/myjobs')  # Redirect to job list after deletion

    return render(request, 'job_delete.html', {'job': job})    
    

def view_applications(request):
    applications = Application.objects.filter(job__employer=request.user)  # Get applications for employer's jobs
    return render(request, 'view_applications.html', {'applications': applications}) 


def viewapplicantdetails(request, v_id):
    application = get_object_or_404(Application, id=v_id)
    
    interview = Interview.objects.filter(application=application).first()

    if request.method == 'POST':
        new_status = request.POST.get('status')  # Get the new status from the form
        application.status = new_status
        application.save()  # Save the updated status
        messages.success(request, f"Application status updated to {application.status}.")
        return redirect('viewapplicantdetails', v_id=v_id)  # Redirect to refresh the page

    context = {
        'application': application,  # Pass the application object
        'applicant_name': application.applicant_fullname or "Not provided",
        'email': application.email or "Not provided",
        'phone': application.phone or "Not provided",
        'skills': application.skills or "Not provided",
        'cover_letter': application.cover_letter,
        'applied_date': application.applied_at,
        'profile_photo': application.profile_photo,
        'status': application.status,
        'interview': interview if application.status == 'selected' else None,  # Pass interview details
    }
    return render(request, 'applicant_detail.html', context)


@login_required
def schedule_interview(request, v_id):
    application = get_object_or_404(Application, id=v_id)

    # Fetch existing interview or create a new one
    interview, created = Interview.objects.get_or_create(application=application, interviewer=request.user)

    if request.method == "POST":
        form = InterviewForm(request.POST, instance=interview)
        if form.is_valid():
            form.save()
            if created:
                messages.success(request, "Interview scheduled successfully!")
            else:
                messages.success(request, "Interview rescheduled successfully!")
            return redirect('viewapplicantdetails', v_id=v_id)  # Redirect to view details
    else:
        form = InterviewForm(instance=interview)

    return render(request, "schedule_interview.html", {"form": form, "application": application, "interview": interview})

@login_required
def delete_interview(request, interview_id):
    interview = get_object_or_404(Interview, id=interview_id, interviewer=request.user)
    interview.delete()
    messages.success(request, "Interview schedule has been deleted successfully.")
    return redirect('viewapplicantdetails', v_id=interview.application.id)  # Redirect back to application details


### my views   jobseeker  dashbord

# job model display
def jobfn(request):
    query = request.GET.get('q', '')  # Get search query from URL parameter
    jobs = Job.objects.all().order_by('-posted_at')  # Fetch all jobs
    categories = JobCategory.objects.all()

    if query:
        jobs = jobs.filter(Q(job_title__icontains=query) | Q(category__name__icontains=query))

    return render(request, 'alljobs.html', {'jobs': jobs,'categories': categories,'query': query})


# view one job
def detailjobfn(request,job_id):
    job = Job.objects.get( id=job_id)
    user_has_applied = Application.objects.filter(job=job, job_seeker=request.user).exists()
    return render(request, 'job_detail.html', {'job': job, "user_has_applied": user_has_applied})


# apply job
@login_required
def applicationformfn(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Check if the job seeker has already applied for this job
    existing_application = Application.objects.filter(job=job, job_seeker=request.user).exists()

    if existing_application:
        messages.error(request, "You have already applied for this job.")
        return redirect("/alljobs/")  # Redirect back to job listings

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.job_seeker = request.user
            application.status = "Pending"
            application.save()
            messages.success(request, "Your application has been submitted successfully!")
            return redirect("/myapplications")  
        else:
            messages.error(request, "There were errors in your application. Please correct them below.")
    else:
        form = ApplicationForm()

    return render(request, "job_apply.html", {"form": form, "job": job, "page_title": "Apply"})



def jobseekerapplications(request):
    applications = Application.objects.filter(job_seeker=request.user)
    return render(request, 'myapplication.html', {'applications': applications})

#edit application
@login_required
def edit_application(request, v_id):
    application = get_object_or_404(Application, id=v_id, job_seeker=request.user)
    job = application.job

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            form.save()
            return redirect('/myapplications')  # Redirect to application list page
    else:
        form = ApplicationForm(instance=application)

    return render(request, "job_apply.html", {"form": form, "job": job, "page_title": "Edit"})
#delete application
@login_required
def delete_application(request, v_id):
    application = get_object_or_404(Application, id=v_id, job_seeker=request.user)

    if request.method == 'POST':
        application.delete()
        return redirect('/myapplications')  # Redirect to application list after deletion

    return render(request, 'delete_application.html', {'application': application})


@login_required
def my_interviews(request):
    interviews = Interview.objects.filter(application__job_seeker=request.user)

    if request.method == "POST":
        interview_id = request.POST.get("interview_id")
        new_status = request.POST.get("status")
        rejection_reason = request.POST.get("rejection_reason", "") if new_status == "rejected" else None

        interview = get_object_or_404(Interview, id=interview_id, application__job_seeker=request.user)
        interview.invitation_status = new_status
        interview.rejection_reason = rejection_reason  # Store rejection reason if applicable
        interview.save()

        messages.success(request, f"Interview status updated to {new_status}.")
        return redirect("my_interviews")  # Refresh page after update

    return render(request, "my_interview.html", {"interviews": interviews})