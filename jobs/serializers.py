from rest_framework import serializers
from .models import User, JobCategory, JobType, Job, Application, Interview

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Using create_user to hash password
        user = User.objects.create_user(**validated_data)
        return user
    

# JobCategory Serializer
class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = '__all__'

# JobType Serializer
class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = '__all__'

# Job Serializer
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

# Application Serializer
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

# Interview Serializer
class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = '__all__'



