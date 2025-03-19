from django.core.mail import send_mail
from django.conf import settings

def send_interview_email(interview):
    job_seeker = interview.application.job_seeker  # Access job seeker via application
    employer = interview.interviewer  # Employer conducting the interview
    job = interview.application.job  # Get the job details

    subject = "Interview Scheduled for Your Job Application"
    message = f"""
    Dear {job_seeker.first_name},

    Your interview for the job **{job.job_title}** has been scheduled.

    📅 **Date:** {interview.interview_date.strftime('%Y-%m-%d %I:%M %p')}
    📍 **Venue:** {interview.venue}
    🏢 **Employer:** {employer.first_name}

    Please be available on time.

    Regards,  
    {employer.first_name}
    """

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,  # Sender Email
        [interview.application.job_seeker.email],  # Recipient Email
        fail_silently=False,
    )