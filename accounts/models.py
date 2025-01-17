from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.core.validators import RegexValidator
# Create your models here.
class MyAccountManager( BaseUserManager ):
    def create_user(self, email,username,blood_group, phone,present_add,permanent_add,last_date_of_donation,password=None,is_staff=False,is_superuser=False ):
        # print('soaib')
        if not username:
            raise ValueError("User must have an username")
        if not phone:
            raise ValueError("User must have a phone number")
        if not blood_group:
            raise ValueError("User must have a  blood_group")
        user = self.model( email = email, username = username , phone = phone, blood_group = blood_group,present_add=present_add,permanent_add=permanent_add,last_date_of_donation=last_date_of_donation)
        user.is_staff = is_staff
        # user.is_admin = is_admin
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save()
        return user

    # def create_staffuser(self, email,username,blood_group, phone,present_add,permanent_add,last_date_of_donation,password=None):
    #     user = self.create_user(email,username,blood_group, phone,present_add,permanent_add,last_date_of_donation,True,False)
    #     return user

    def create_superuser(self,username,password=None):
        user = self.model(username=username,is_staff = True,is_superuser = True)
        user.set_password(password)
        user.save()
        return user



class Account( AbstractBaseUser ):
    email_validate =RegexValidator(regex=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", message="Please enter a valid email.")

    email = models.EmailField( max_length=45, unique = True ,null=True, validators=[email_validate])
    username = models.CharField( max_length=45,  unique = True )
    blood_group  = models.CharField( max_length = 5,null=True )
    phone  = models.CharField( max_length=20, unique = True ,null=True)
    address = models.CharField(max_length = 200,null=True)
    last_date_of_donation = models.DateField(max_length = 50,null=True)
    image = models.ImageField(upload_to ='image/account/%Y/%m/%d',default='avatar.jpg')
    donate = models.PositiveIntegerField(default=0)
    is_admin = models.BooleanField(default = False,null=True)
    is_active = models.BooleanField( default= True,null=True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['']

    objects = MyAccountManager()
    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, boj = None):
        return self.is_superuser

    def has_module_perm(self, app_level):
        if self.is_superuser:
            return True
        return False
    def has_module_perms(self, perms, obj=None):
	    return all(self.has_perm(perm, obj) for perm in perms)
    # def  __init__ ( self , * args , ** kwargs ):
    #     if  " max_length "  not  in kwargs: kwargs [ " max_length " ] =  100
    #     if  " validators "  not  in kwargs: kwargs [ " validators " ] = [validators.RegexValidator ( r " [ 0-9a-zA-Z_. \ - ] {2,50} [ @ ] {1} [ 0-9a- zA-Z_./- ] {2,50} [ . ] {1} [ a-zA-Z ] {2,5} " )]
    #     super (EmailAddressTypeField, self ). __init__ ( * args, ** kwargs)

