import pytest
from django.test import TestCase
from main.models import *
from main.views import *


class test_check_hospital_exist(TestCase):
    def test_hospital_name(self):
        TTS = Hospital.objects.get(name="Tan Tock Seng Hospital")
        self.assertEqual(TTS.name, "Tan Tock Seng Hospital")

class test_items(TestCase):
    def setUp(self):
        Items.objects.create(product_name="Scalpel")
    
    def test_item_name(self):
        scap = Items.objects.get(product_name="Scalpel")
        self.assertEqual(scap.product_name, "Scalpel")

class test_inventory(TestCase):
    def setUp(self):
        Items.objects.create(product_name="Scalpel")
        scap = Items.objects.get(product_name="Scalpel")
        TTS = Hospital.objects.get(name="Tan Tock Seng Hospital")
        Inventory.objects.create(hospital=TTS , item=scap , quantity=0, status= "None" )
    
    def test_item_name(self):
        scap = Items.objects.get(product_name="Scalpel")
        scap_inv = Inventory.objects.get(item=scap.id)
        self.assertEqual(scap_inv.hospital.name, "Tan Tock Seng Hospital" )
        self.assertEqual(scap_inv.item.product_name, "Scalpel")
        self.assertEqual(scap_inv.quantity, 0)
        self.assertEqual(scap_inv.status, "None")

class test_request(TestCase):
    def setUp(self):
        Items.objects.create(product_name="Scalpel")
        scap = Items.objects.get(product_name="Scalpel")
        TTS = Hospital.objects.get(name="Tan Tock Seng Hospital")
        RH = Hospital.objects.get(name="Raffles Hospital")
        inv = Inventory.objects.create(hospital=TTS , item=scap , quantity=0, status= "None" )
        Requests.objects.create(inventory=inv, requestBy=TTS.id,requestAcceptedFrom=RH.id)

    
    def test_item_name(self):
        scap = Items.objects.get(product_name="Scalpel")
        scap_inv = Inventory.objects.get(item=scap.id)
        TTS = Hospital.objects.get(name="Tan Tock Seng Hospital")
        RH = Hospital.objects.get(name="Raffles Hospital")
        req = Requests.objects.get(inventory=scap_inv, requestBy=TTS.id,requestAcceptedFrom=RH.id)
        self.assertEqual(req.inventory.item.product_name, "Scalpel" )
        self.assertEqual(req.requestBy, TTS.id )
        self.assertEqual(req.requestAcceptedFrom, RH.id )
