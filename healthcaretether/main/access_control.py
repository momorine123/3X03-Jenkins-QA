from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Hospital, Items, Inventory, Requests, AccountManagement

from main.views import *

import logging
logger = logging.getLogger('access_control')

def setPermissions():

    admin_group, created = Group.objects.get_or_create(name="Administrator")
    manager_group, created = Group.objects.get_or_create(name="Manager")
    staff_group, created = Group.objects.get_or_create(name="Staff")

    content_type = ContentType.objects.get_for_model(Items)
    item_permission = Permission.objects.filter(content_type=content_type)

    for perm in item_permission:
        if perm.codename == "add_assets":
            admin_group.permissions.add(perm)

        elif perm.codename == "update_assets":
            admin_group.permissions.add(perm)

        elif perm.codename == "delete_assets":
            admin_group.permissions.add(perm)
    
    content_type = ContentType.objects.get_for_model(Inventory)
    inv_permission = Permission.objects.filter(content_type=content_type)

    for perm in inv_permission:
        if perm.codename == "inventory_management":
            manager_group.permissions.add(perm)

        elif perm.codename == "inventory_list":
            manager_group.permissions.add(perm)

        elif perm.codename == "manager_update_assets":
            manager_group.permissions.add(perm)

        elif perm.codename == "manager_delete_assets":
            manager_group.permissions.add(perm)

        elif perm.codename == "select_list":
            manager_group.permissions.add(perm)

        elif perm.codename == "select":
            manager_group.permissions.add(perm)

    content_type = ContentType.objects.get_for_model(Requests)
    request_permission = Permission.objects.filter(content_type=content_type)

    for perm in request_permission:
        if perm.codename == "requested_list":
            staff_group.permissions.add(perm)

        elif perm.codename == "staff_request":
            staff_group.permissions.add(perm)

        elif perm.codename == "request_to":
            manager_group.permissions.add(perm)

        elif perm.codename == "manager_update_request_to":
            manager_group.permissions.add(perm)

        elif perm.codename == "manager_delete_request_to":
            manager_group.permissions.add(perm)

        elif perm.codename == "request_from_list":
            manager_group.permissions.add(perm)

        elif perm.codename == "manager_request_from":
            manager_group.permissions.add(perm)

        elif perm.codename == "approve":
            manager_group.permissions.add(perm)

    content_type = ContentType.objects.get_for_model(AccountManagement)
    accountManagement_permission = Permission.objects.filter(content_type=content_type)
    
    logger.error([perm.codename for perm in accountManagement_permission])

    for perm in accountManagement_permission:

        if perm.codename == "it_home":
            admin_group.permissions.add(perm)

        elif perm.codename == "manager_home":
            manager_group.permissions.add(perm)

        elif perm.codename == "staff_home":
            staff_group.permissions.add(perm)

        elif perm.codename == "account_management":
            admin_group.permissions.add(perm)

        elif perm.codename == "register_request":
            admin_group.permissions.add(perm)

        elif perm.codename == "update_request":
            admin_group.permissions.add(perm)

        elif perm.codename == "update_password":
            admin_group.permissions.add(perm)

        elif perm.codename == "unlock_username":
            admin_group.permissions.add(perm)

        elif perm.codename == "unlock_ip":
            admin_group.permissions.add(perm)

    return admin_group, manager_group, staff_group