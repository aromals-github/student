from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from . models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication


class SignUp(APIView):
    
    serializer_class    =  SignUpSerializer
    permission_classes = []
    
    def post(self,request:Request):
        
        data = request.data
        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"Success":"Regular User is Created"},status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
    
class LoginView(APIView):
    
    permission_classes = []
    
    def get(self,request: Request):
         
        email      = request.data.get("email")
        password   = request.data.get("password")
        user       = authenticate(email=email,password=password)
    
        if user is not None:
            token = Token.objects.get(user=user)
            return Response({"Success":"Logged In","token":str(token)})
        return Response({"Error":"User doent not exists"})


       
class Student_Details(APIView):
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_classes = StudentSerializer
    
    def post (self, request,*args,**kwargs):
        
            if not request.user.is_superuser:
                serializer = StudentSerializer(data=request.data)
                if serializer.is_valid():
                    d = serializer.save(admin=request.user)
                    Approval.objects.create(student=d)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)
            
            
    def put(self,request,pk,*args,**kwargs):
        
        try :   
            if Approval.objects.filter(student=pk,status=True):
                if Student_Info.objects.filter(id=pk,is_verified=False,admin=request.user.id):
                    student = Student_Info.objects.get(id=pk)
                    serializer = StudentSerializer(student,data=request.data)
                    if serializer.is_valid():
                        c = serializer.save()
                        c.is_verified=True
                        c.save()
                        return Response(serializer.data)
                    else:
                        return Response(serializer.errors)
                    
                else:
                    return Response({"ERROR":"You are not the admin for this student or Already verified."})
            else:
                return Response({"Message":"Not yet approved by the super user."})
        
        except Exception as e :
            return Response({"Error":f"{e}"})
            
            
class Unverified_Students(APIView):
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_classes = StudentSerializer
    
    def get(self,request,*args,**kwargs):
        
        if request.user.is_superuser:
            queryset = Student_Info.objects.filter(is_verified=False)
            serializer = StudentSerializer(queryset,many=True)
            return Response(serializer.data)
        else:
            return Response({"Not an superuser"})
        
    def post(self,request,pk,*args,**kwargs):
        
        if request.user.is_superuser:
            if Approval.objects.filter(student=pk,status=False):
                Approval.objects.filter(student=pk, status=False).update(status=True)
                return Response({"Success":"Approved"})
            else:
                Approval.objects.filter(student=pk, status=True).update(status=False)
                return Response({"Success":"Rejected"})
        else:
            return Response ({"User Error":"You are not a super user."})

        

    

