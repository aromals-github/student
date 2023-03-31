

from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from rest_framework.authtoken.models import Token

class AccountsManager(BaseUserManager):
    
    use_in_migrations = True
    
    def create_user(self,email,username,password=None):
        
        if not email:
            raise ValueError("Users must have an valid email address.")
        if not username :
            raise ValueError("User must have unique username.")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user 
    

    def create_superuser(self,email,username,password):
        user =  self.create_user(
                                    email = self.normalize_email(email),
                                    username = username,
                                    password = password,
                            )
        
        user.is_admin       = True
        user.is_staff       = True
        user.is_superuser   = True
        
        user.save()
        return user
        


class Accounts(AbstractBaseUser):
    
    username        = models.CharField(max_length=30 ,unique = True)
    email           = models.EmailField(verbose_name='email', max_length=60 ,unique = True)
   
    
    is_superuser    = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_admin        = models.BooleanField(default=False)
    
    objects = AccountsManager()
    
    USERNAME_FIELD      = 'email'
    REQUIRED_FIELDS     = ['username']
    
    def has_perm(self,perm,obj = None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def __str__(self):
        return self.username
    class Meta:
        verbose_name_plural = "Accounts"
        
        
class Student_Info(models.Model):
    
    admin       = models.ForeignKey(Accounts,on_delete=models.CASCADE,blank=False,null=False)
    name        = models.CharField(max_length=30,blank=False,null=False)
    photo       = models.ImageField(upload_to="student-image",blank=True,null=True)
    age         = models.IntegerField(blank=True,null=True)
    address     = models.CharField(max_length=80,blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural ="Student Info"
        
    def save(self, *args, **kwargs):
        if self.pk is not None: 
            super(Student_Info, self).save(*args, **kwargs) 
        elif self.admin.is_superuser: 
            super(Student_Info, self).save(*args, **kwargs)
        else:
            self.age = None
            self.address = None
            super(Student_Info, self).save(*args, **kwargs)
            
            
    
class Approval(models.Model):
    
    student     = models.ForeignKey(Student_Info,on_delete=models.CASCADE,null=False,blank=False)
    status      = models.BooleanField(default=False)
    
    def __str__(self):
        return self.student.name
    
    class Meta:
        verbose_name_plural = "Approve Students"