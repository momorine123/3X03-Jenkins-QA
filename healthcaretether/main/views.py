from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .forms import addItemForm, managerItemForm, CustomUserCreationForm,CustomUserChangeForm, CustomChangeFormPassword,UnlockIPForm,UnlockUsernameForm

from .models import Items, CustomUser, Inventory, Requests
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from axes.utils import reset
from django.conf import settings
import urllib.request
import json

from main.access_control import setPermissions

import logging
logger = logging.getLogger('main')

# Create your views here.

#authentication
def loginView(request):
    context={}
    if request.method=="POST":

        #reCAPTCHA validation
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())

        if result['success']:
            username=request.POST["username"]
            password=request.POST["password"]
            user=authenticate(request,username=username,password=password)


            if user:
                from mfa.helpers import has_mfa
                res = has_mfa(username = username, request = request)  # has_mfa returns false or HttpResponseRedirect
                if res:
                    return res
                return create_session(request,user.username)
        failed_message = "Login failed with username: {} ,password: {}, headers: {}".format(request.POST["username"], request.POST["password"], request.META)
        logger.error(failed_message)
        context["invalid"]=True
    return render(request, "registration/login.html", context)

def create_session(request,username):
    user=CustomUser.objects.get(username=username)
    user.backend='django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return HttpResponseRedirect(reverse('dashboardRedirect'))
    

def logoutView(request):
    logout(request)
    return render(request,"registration/logout.html",{})


def wrong_user(request):
    message = "User " + request.user.username + " not authorised to access page"
    logger.error(message)
    return render(request,"wrong_user.html")


@login_required()
def mfa_redirect(request):
    return redirect('dashboardRedirect')


#@login_required(login_url='/auth/login/')
@login_required()
def dashboardRedirect(request):
    current_user = request.user
    current_user.groups.clear()
    admin_group, manager_group, staff_group = setPermissions()
    message = "User " + current_user.username + " has logged in"
    logger.info(message)
    success_message = "Login sucess with username: {}, headers: {}".format(current_user.username, request.META)
    logger.info(success_message)
    if current_user.role == "S":
        current_user.groups.add(staff_group)
        return redirect('/staff/home/')
    elif current_user.role == "M":
        current_user.groups.add(manager_group)
        return redirect('/manager/home/')
    elif current_user.role == "A":
        current_user.groups.add(admin_group)
        return redirect('/it/home/')



#admin views
#admin display item list
#@login_required(login_url='/auth/login/')
@login_required()
def it_home(request):
    if not request.user.has_perm("main.it_home"):
        message = request.user.username + " tried to access the IT it_home page."
        logger.error(message)
        return redirect("/wrong_user/")

    items = Items.objects.all()
    context = {'items' : items}
    return render(request,'IT/item_management.html', context)



#@login_required(login_url='/auth/login/')
@login_required()
def account_management(request):
    if not request.user.has_perm("main.account_management"):
        message = request.user.username + " tried to access the IT account_management page."
        logger.error(message)
        return redirect("/wrong_user/")

    users = CustomUser.objects.all()
    context = {'users' : users}
    return render(request,'IT/account_management.html', context)

def register_request(request):
    if not request.user.has_perm("main.register_request"):
        message = request.user.username + " tried to access the IT register_request page."
        logger.error(message)
        return redirect("/wrong_user/")
    else:
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(request, "Registration successful." )
                return redirect("/it/accounts/") 
            messages.error(request, "Unsuccessful registration. Invalid information.")
        form = CustomUserCreationForm()
        return render (request,"registration/register.html", context={"register_form":form})

def update_request(request,slug):
    if not request.user.has_perm("main.update_request"):
        message = request.user.username + " tried to access the IT update_request page."
        logger.error(message)
        return redirect("/wrong_user/")

    slug = get_object_or_404(CustomUser,slug=slug)
    user = CustomUser.objects.get(id = slug.id)
    form = CustomUserChangeForm(instance=user)

    currentrole = user.role
    currentusername = user.username

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():

            if currentrole != form.cleaned_data['role']:
                if form.cleaned_data[role] == "S":
                    role = "Staff"
                elif form.cleaned_data[role] == "M":
                    role = "Manager"
                elif form.cleaned_data[role] == "A":
                    role = "Admin"

                message = "Admin " + request.user.username + " has changed " + currentusername + "'s role' to " + role
                logger.info(message)

            form.save()
            message = "Admin " + request.user.username + " updated " + currentusername
            logger.info(message)
            return redirect('account-management')

    context = {'update_form' : form}
    return render(request, 'registration/update.html', context)

def update_password(request,slug):
    if not request.user.has_perm("main.update_password"):
        message = request.user.username + " tried to access the IT update_password page."
        logger.error(message)
        return redirect("/wrong_user/")
    slug = get_object_or_404(CustomUser,slug=slug)
    user = CustomUser.objects.get(id = slug.id)
    form = CustomChangeFormPassword(user)
    if request.method == 'POST':
        form = CustomChangeFormPassword(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password has been changed")
            return redirect('account-management')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = CustomChangeFormPassword(user)
    context = {'update_password_form' : form}
    return render(request, 'registration/password.html', context)


#admin add item
#@login_required(login_url='auth/login/')
@login_required()
def add_assets(request):
    if not request.user.has_perm("main.add_assets"):
        message = request.user.username + " tried to access the IT add_assets page."
        logger.error(message)
        return redirect("/wrong_user/")

    form = addItemForm()
    if request.method == 'POST':
        form = addItemForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Admin " + request.user.username + " added item"
            logger.info(message)
            return redirect('it-home')
    
    context = {'form' : form}
    return render(request,'IT/add_assets.html', context)

#admin Update item

@login_required(login_url='auth/login/')
def update_assets(request, slug):
    if not request.user.has_perm("main.update_assets"):
        message = request.user.username + " tried to access the IT update_assets page."
        logger.error(message)
        return redirect("/wrong_user/")
    slug = get_object_or_404(Items,slug=slug)
    item = Items.objects.get(id = slug.id)
    form = addItemForm(instance=item)

    if request.method == 'POST':
        form = addItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            message = "Admin " + request.user.username + " updated item"
            logger.info(message)
            return redirect('it-home')

    context = {'form' : form}
    return render(request, 'IT/add_assets.html', context)

#admin Delete item
@login_required(login_url='auth/login/')
def delete_assets(request, slug):
    if not request.user.has_perm("main.delete_assets"):
        message = request.user.username + " tried to access the IT delete_assets page."
        logger.error(message)
        return redirect("/wrong_user/")
    
    slug = get_object_or_404(Items,slug=slug)
    item = Items.objects.get(id=slug.id)
    if request.method == 'POST':
        item.delete()
        message = "Admin " + request.user.username + "deleted item"
        logger.info(message)
        return redirect('it-home')
    return render(request, 'delete.html', {'obj' : item})


#admin reset axes lockout
def unlock_username(request):
    if not request.user.has_perm("main.unlock_username"):
        message = request.user.username + " tried to access the IT unlock_username page."
        logger.error(message)
        return redirect("/wrong_user/")

    if request.method == 'POST':
        form = UnlockUsernameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username_to_unlock")
            reset(username = username)
            message = username +" unlocked"
            return redirect('account-management')
    else:
        form = UnlockUsernameForm()
    return render(request, 'IT/unlock_username.html',{'form': form})

def unlock_ip(request):
    if not request.user.has_perm("main.unlock_ip"):
        message = request.user.username + " tried to access the IT unlock_ip page."
        logger.error(message)
        return redirect("/wrong_user/")

    if request.method == 'POST':
        form = UnlockIPForm(request.POST)
        if form.is_valid():
            ip = form.cleaned_data.get("ip_to_unlock")
            reset(ip= ip)
            message = ip +" unlocked"
            return redirect('account-management')
    else:
        form = UnlockIPForm()
    return render(request, 'IT/unlock_ip.html',{'form': form})

#admin views ends



#staff views
#staff Display hospital inventory list
#@login_required(login_url='/auth/login/')
@login_required()
def staff_home(request):
    if not request.user.has_perm("main.staff_home"):
        message = request.user.username + " tried to access the Staff staff_home page."
        logger.error(message)
        return redirect("/wrong_user/")

    userHospID = request.user.hospital
    items = Inventory.objects.filter(hospital_id = userHospID)
    context = {'items' : items}
    return render(request,'staff/asset_list.html', context)

#staff Display REQUESTED hospital inventory list
#@login_required(login_url='/auth/login/')
@login_required()
def requested_list(request):
    if not request.user.has_perm("main.requested_list"):
        message = request.user.username + " tried to access the Staff requested_list page."
        logger.error(message)
        return redirect("/wrong_user/")

    userHospID = request.user.hospital
    items = Inventory.objects.filter(hospital_id = userHospID).filter(status__in=["Submitted","Pending"])
    context = {'reqs' : items}
    return render(request,'staff/requested_list.html', context)

#staff Change inventory status to SUBMITTED
@login_required(login_url='/auth/login/')
def staff_request(request,slug):
    if not request.user.has_perm("main.staff_request"):
        message = request.user.username + " tried to access the Staff staff_request page."
        logger.error(message)
        return redirect("/wrong_user/")

    slug = get_object_or_404(Items,slug=slug)
    slugid = Items.objects.get(id = slug.id)
    userHospID = request.user.hospital
    inv = Inventory.objects.filter(hospital_id = userHospID).get(item_id = slugid)
    inv.status = "Submitted"
    inv.save(update_fields=['status'])
    return redirect('staff-home') 

#staff views ends



#mananger views
#mananger Display request management page
#@login_required(login_url='/auth/login/')
@login_required()
def manager_home(request):
    if not request.user.has_perm("main.manager_home"):
        message = request.user.username + " tried to access the Manager manager_home page."
        logger.error(message)
        return redirect("/wrong_user/")
    return render(request,'manager/request_management.html')

#mananger Display inventory management page
#@login_required(login_url='/auth/login/')
@login_required()
def inventory_management(request):
    if not request.user.has_perm("main.inventory_management"):
        message = request.user.username + " tried to access the Manager inventory_management page."
        logger.error(message)
        return redirect("/wrong_user/")
    return render(request, 'manager/inventory_management.html')

#mananger Display hospital inventory list
#@login_required(login_url='/auth/login/')
@login_required()
def inventory_list(request):
    if not request.user.has_perm("main.inventory_list"):
        message = request.user.username + " tried to access the Manager inventory_list page."
        logger.error(message)
        return redirect("/wrong_user/")
    
    userHospID = request.user.hospital
    items = Inventory.objects.filter(hospital_id = userHospID)
    context = {'items' : items}
    return render(request, 'manager/inventory_list.html', context)

#mananger Update inventory item
@login_required(login_url='auth/login/')
def manager_update_assets(request, slug):
    if not request.user.has_perm("main.manager_update_assets"):
        message = request.user.username + " tried to access the Manager manager_update_assets page."
        logger.error(message)
        return redirect("/wrong_user/")
    
    userHospID = request.user.hospital
    slug = get_object_or_404(Items,slug=slug)
    item = Inventory.objects.filter(hospital_id = userHospID).get(item_id = slug)
    form = managerItemForm(instance=item)

    if request.method == 'POST':
        form = managerItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            message = "Manager " + request.user.username + "updated inventory item"
            logger.info(message)
            return redirect('inventory-list')

    context = {'form' : form}
    return render(request, 'manager/manage_asset.html', context)

#mananger Delete inventory item
@login_required(login_url='auth/login/')
def manager_delete_assets(request, slug):
    if not request.user.has_perm("main.manager_delete_assets"):
        message = request.user.username + " tried to access the Manager manager_delete_assets page."
        logger.error(message)
        return redirect("/wrong_user/")
    userHospID = request.user.hospital
    slug = get_object_or_404(Items,slug=slug)
    item = Inventory.objects.filter(hospital_id = userHospID).get(item_id=slug)
    if request.method == 'POST':
        item.delete()
        message = "Manager " + request.user.username + "deleted inventory item"
        logger.info(message)
        return redirect('inventory-list')
    return render(request, 'delete.html', {'obj' : item})

#mananger view inventory item that can be selected
#@login_required(login_url='/auth/login/')
@login_required()
def select_list(request):
    if not request.user.has_perm("main.select_list"):
        message = request.user.username + " tried to access the Manager select_list page."
        logger.error(message)
        return redirect("/wrong_user/")
    
    userHospID = request.user.hospital
    inv = Inventory.objects.filter(hospital = userHospID).values_list('item_id')
    items = Items.objects.exclude(id__in = inv )
    context = {'items' : items}
    return render(request, 'manager/select_asset.html', context)

#mananger Select item from Global List
@login_required(login_url='/auth/login/')
def select(request,slug):
    if not request.user.has_perm("main.select"):
        message = request.user.username + " tried to access the Manager select page."
        logger.error(message)
        return redirect("/wrong_user/")
    
    slug = get_object_or_404(Items,slug=slug)
    slugid = Items.objects.get(id = slug.id)
    userHospID = request.user.hospital
    # item = Items.objects.get(id = pk)
    inv = Inventory(hospital = userHospID , item = slugid , quantity = 0, status = "None")
    inv.save()
    return redirect('select-list') 

#mananger Request that were made by staff
#@login_required(login_url='/auth/login/')
@login_required()
def request_to(request):
    if not request.user.has_perm("main.request_to"):
        message = request.user.username + " tried to access the Manager request_to page."
        logger.error(message)
        return redirect("/wrong_user/")

    userHospID = request.user.hospital
    items = Inventory.objects.filter(hospital_id = userHospID).filter(status__in=["Submitted","Pending"])
    context = {'items' : items}
    return render(request,'manager/request_to.html', context)

#mananger Update the staff requested item status to PENDING and include in REQUEST TABLE
@login_required(login_url='/auth/login/')
def manager_update_request_to(request,slug):
    if not request.user.has_perm("main.manager_update_request_to"):
        message = request.user.username + " tried to access the Manager manager_update_request_to page."
        logger.error(message)
        return redirect("/wrong_user/")

    slug = get_object_or_404(Items,slug=slug)
    slugid = Items.objects.get(id = slug.id)
    userHospID = request.user.hospital
    inv = Inventory.objects.filter(hospital_id = userHospID).get(item_id = slugid)
    inv.status = "Pending"
    inv.save(update_fields=['status'])
    req = Requests(inventory= inv, requestBy = userHospID.id, requestAcceptedFrom = 0)
    req.save()

    return redirect('request-to')

#mananger Update the staff requested item status to NONE
@login_required(login_url='/auth/login/')
def manager_delete_request_to(request,slug):
    if not request.user.has_perm("main.manager_delete_request_to"):
        message = request.user.username + " tried to access the Manager manager_delete_request_to page."
        logger.error(message)
        return redirect("/wrong_user/")

    slug = get_object_or_404(Items,slug=slug)
    slugid = Items.objects.get(id = slug.id)
    userHospID = request.user.hospital
    req = Inventory.objects.filter(hospital_id = userHospID).get(item_id = slugid)
    req.status = "None"
    req.save(update_fields=['status'])
    return redirect('request-to')

#mananger Display Requested item from other hospital that has not been accepted
#@login_required(login_url='/auth/login/')
@login_required()
def request_from_list(request):
    if not request.user.has_perm("main.request_from_list"):
        message = request.user.username + " tried to access the Manager request_from_list page."
        logger.error(message)
        return redirect("/wrong_user/")

    userHospID = request.user.hospital
    inv = Inventory.objects.filter(hospital_id = userHospID).values('item_id')
    req = Requests.objects.filter(requestAcceptedFrom = 0).exclude(requestBy = userHospID.id).filter(inventory__item__in = inv)
    context = {'reqs' : req, 'invs': inv}
    return render(request,'manager/request_from.html', context)

#mananger Update the REQUEST TABLE field "requestedAcceptedFrom" with the hosp ID and the item inventory status to NONE
@login_required(login_url='/auth/login/')
def manager_request_from(request, slug):
    if not request.user.has_perm("main.manager_request_from"):
        message = request.user.username + " tried to access the Manager manager_request_from page."
        logger.error(message)
        return redirect("/wrong_user/")


    userHospID = request.user.hospital
    slug = get_object_or_404(Items,slug=slug)
    slugid = Items.objects.get(id = slug.id)
    invslug = Inventory.objects.filter(item_id = slugid)
    req = Requests.objects.get(inventory__in = invslug)

    inv = Inventory.objects.filter(hospital_id = req.requestBy).get(item_id = slugid)
    inv.status = "None"
    inv.save(update_fields=['status'])
    req.requestAcceptedFrom = userHospID.id
    req.save(update_fields=['requestAcceptedFrom'])
    return redirect('request-from')

#mananger APPROVE request by other hospital
@login_required(login_url='/auth/login/')
def approve(request, slug):
    if not request.user.has_perm("main.approve"):
        message = request.user.username + " tried to access the Manager approve page."
        logger.error(message)
        return redirect("/wrong_user/")

    userHospID = request.user.hospital
    slug = get_object_or_404(Items,slug=slug)
    slugid = Items.objects.get(id = slug.id)
    invslug = Inventory.objects.filter(item_id = slugid)
    req = Requests.objects.get(inventory__in = invslug)
    item = Items.objects.get(product_name = req.inventory)
    inv = Inventory.objects.filter(hospital_id = userHospID).get(item = item)
    context = {'reqs' : req, 'invs' : inv}
    return render(request,'manager/approve.html', context)

#mananger views Ends