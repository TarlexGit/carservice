from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Profile
from rest_framework.validators import UniqueValidator 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):     
    def validate(self, attr):
        data = super().validate(attr)
        print(attr)
        data = self.get_token(self.user)
        data['user'] = str(self.user.id) 
        data['id'] = str(self.user.id) 
        context = {'user': data['user'], 'token': str(data) }  
        return context

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']



from rest_framework_simplejwt.authentication import JWTAuthentication
class CreateUserProfileSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Profile
        fields = '__all__'  
 
class ProfileUpdate(serializers.ModelSerializer): 
    class Meta:
        model = Profile
        fields = '__all__'
    # def update(self, instance, validated_data): 
    #     demo = Profile.objects.get(pk=instance.id)
    #     Profile.objects.filter(pk=instance.id)\
    #                        .update(**validated_data)
    #     return demo 
    def update(self, instance, validated_data):
        # instance.user = validated_data.get('user', instance.id)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.father_name = validated_data.get('father_name', instance.father_name)
        instance.car_mark = validated_data.get('car_mark', instance.car_mark)
        print(instance.id)
        print(validated_data)
        instance.save()
        return instance


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=User.objects.all())]
            )  
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User(email=validated_data['email'],
                username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password' )


