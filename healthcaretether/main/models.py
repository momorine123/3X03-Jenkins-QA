from datetime import datetime
from random import choice, choices
from re import M

from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

#hospital model
class Hospital(models.Model):
    
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name

#items model
class Items(models.Model):
    
    class Meta: 
        permissions = [
            ("add_assets","Admin can add assets to the system"),
            ("update_assets","Admin can update asset details"),
            ("delete_assets","Admin can delete assets from system")
        ]

    product_name = models.CharField(max_length=40)
    slug = models.SlugField(null=True, unique=True, max_length=40)

    def name(self):
        return self.product_name
    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):  # new
        self.slug = slugify(self.product_name)
        return super().save(*args, **kwargs)

#inventory model
class Inventory(models.Model):
    
    class Meta:
        permissions = [
            ("inventory_management", "Manager can manage inventory"),
            ("inventory_list", "Manager can view inventory"),
            ("manager_update_assets", "Manager can update inventory information"),
            ("manager_delete_assets", "Manager can delete inventory"),
            ("select_list", "Manager can select inventory"),
            ("select", "Manager can selct from global inventory")
        ]

    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    item = models.ForeignKey(Items,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length = 9)

    def itemName(self):
        return self.item.product_name

    def itemId(self):
        return self.item.id
    
    def __str__(self):
        return self.item.product_name
    
    def slugName(self):
        return self.item.slug


#request model
class Requests(models.Model):
    
    class Meta:
        permissions = [
            ("requested_list", "Staff can view request list"),
            ("staff_request", "Staff can request for inventory"),
            ("request_to", "Manager can view requests by staff"),
            ("manager_update_request_to", "Manager can update the request for inventory"),
            ("manager_delete_request_to", "Manager can delete the request for inventory"),
            ("request_from_list", "Manager can view the list of external requests"),
            ("manager_request_from", "Manager can edit the external request"),
            ("approve", "Manager can approve the external request")
        ]
 
    inventory = models.ForeignKey(Inventory,on_delete=models.CASCADE)
    requestBy = models.IntegerField()
    requestAcceptedFrom = models.IntegerField()

    def invName(self):
        return self.inventory.item

    def invQty(self):
        return self.inventory.quantity
    
    def invStatus(self):
        return self.inventory.status
    
    def invHosp(self):
        return self.inventory.hospital

    def invitemId(self):
        return self.inventory.item_id
    
    def slugName(self):
        return self.inventory.item.slug

#custom user model
class CustomUser(AbstractBaseUser,PermissionsMixin):

    username = models.CharField(max_length=30, unique=True, validators=[RegexValidator(regex="^[a-zA-Z0-9_]*$", message="Only Alphanumeric and Underscore Allowed!")])
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    first_name = 'a'
    last_name = 'b'
    ROLE_CHOICES = [
        ("S","Staff"),
        ("M","Manager"),
        ("A","Admin")
    ]
    role = models.CharField(max_length=1,choices = ROLE_CHOICES, default="S")
    slug = models.SlugField(null=True, unique=True, max_length=40)
    

    # hospital = Hospital.objects.all()
    # HOSPITAL_CHOICES = [
    #     (1,hospital[0].name),
    #     (2,hospital[1].name),
    #     (3,hospital[2].name),
    #     (4,hospital[3].name),
    #     (5,hospital[4].name),
    #     (6,hospital[5].name),
    # ]

    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE, null=True)
    passwordChangedAt = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    def save(self, *args, **kwargs):  # new
        self.slug = slugify(self.username)
        return super().save(*args, **kwargs)

class AccountManagement(models.Model):
    
    class Meta:
        permissions = [
            ("it_home", "Admin can view IT home page"),
            ("manager_home", "Manager can view Manager home page"),
            ("staff_home", "Staff can view Staff home page"),
            ("account_management", "Admin can view account details"),
            ("register_request", "Admin can register accounts to system"),
            ("update_request","Admin can update account details"),
            ("update_password","Admin can update account password"),
            ("unlock_username","Admin can unlock a locked out account"),
            ("unlock_ip","Admin can unlock a locked out ip")
        ]
