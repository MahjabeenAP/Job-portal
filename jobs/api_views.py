from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from .models import User, JobCategory, JobType, Job, Application, Interview
from .serializers import UserSerializer, JobCategorySerializer, JobTypeSerializer, JobSerializer, ApplicationSerializer, InterviewSerializer
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authentication import TokenAuthentication


# REGISTER APIs
@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any user to register without authentication
def apiregisterfn(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])  # Encrypt password
        user.save()

        # Generate token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# LOGIN APIs
@api_view(['POST'])
@permission_classes([AllowAny]) 
def apiloginfn(request):
    user = get_object_or_404(User, username=request.data['username'])
    
    if not user.check_password(request.data['password']):
        return Response({"detail": "Invalid username or password."}, status=status.HTTP_404_NOT_FOUND)

    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    
    return Response({"token": token.key, "user": serializer.data})



# LOGOUT APIs
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def apilogoutfn(request):
    try:
        request.auth.delete()  # Delete the token for logout
        return Response({"message": "Successfully logged out!"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


#  USER APIs
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_list_create(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# JOB CATEGORY APIs
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def jobcategory_list_create(request):
    if request.method == 'GET':
        categories = JobCategory.objects.all()
        serializer = JobCategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = JobCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def jobcategory_detail(request, pk):
    try:
        category = JobCategory.objects.get(pk=pk)
    except JobCategory.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JobCategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = JobCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    
    

#  JOB TYPE APIs
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def jobtype_list_create(request):
    if request.method == 'GET':
        jobtypes = JobType.objects.all()
        serializer = JobTypeSerializer(jobtypes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = JobTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def jobtype_detail(request, pk):
    try:
        jobtype = JobType.objects.get(pk=pk)
    except JobType.DoesNotExist:
        return Response({"error": "Job Type not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JobTypeSerializer(jobtype)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = JobTypeSerializer(jobtype, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        jobtype.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    


# JOB APIs
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def job_list_create(request):
    if request.method == 'GET':
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def job_detail(request, pk):
    try:
        job = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JobSerializer(job)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        job.delete()
        return Response({"message": "Job deleted successfully"},status=status.HTTP_204_NO_CONTENT)


#  APPLICATION APIs
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def application_list_create(request):
    if request.method == 'GET':
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def application_detail(request, pk):
    try:
        application = Application.objects.get(pk=pk)
    except Application.DoesNotExist:
        return Response({"error": "Application not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ApplicationSerializer(application)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ApplicationSerializer(application, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        application.delete()
        return Response({"message": "Application deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)



#  INTERVIEW APIs
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def interview_list_create(request):
    if request.method == 'GET':
        interviews = Interview.objects.all()
        serializer = InterviewSerializer(interviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = InterviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def interview_detail(request, pk):
    try:
        interview = Interview.objects.get(pk=pk)
    except Interview.DoesNotExist:
        return Response({"error": "Interview not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InterviewSerializer(interview)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = InterviewSerializer(interview, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        interview.delete()
        return Response({"message": "deleted successfully"},status=status.HTTP_204_NO_CONTENT)
    

