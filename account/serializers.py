from rest_framework import serializers
from .models import *



class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model           = Accounts
        fields          = ('email','username','password')
        extra_kwargs    = {'passwords': {'write_only':True, 'required':True}}
 
        
    def create(self,validated_data):
        user            = Accounts.objects.create_user(**validated_data)
        return user
    
class StudentSerializer(serializers.ModelSerializer):
    
    class Meta:
       model =  Student_Info
       fields = ( 'id','name', 'photo','age','address','is_verified')
       

       