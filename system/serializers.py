from rest_framework import serializers
from .models import Department, Role, User

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['id','username','first_name','last_name','email','phone','department','roles']
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone']
