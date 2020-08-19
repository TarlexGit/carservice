from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator 
from users.models import Profile
from .models import Master, FixDate
from .services import chek_work_time
import datetime
from rest_framework import serializers


class MasterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Master
        fields = ['url', 'first_name', 'father_name']

class SignUpSerializer(serializers.ModelSerializer): 
    class Meta:
        model = FixDate
        fields= ('master', 'profile', 'start_date', 'start_time', 'end_time')
    
    # def create(self, validated_data):
    #     return FixDate.objects.create(**validated_data)
