# from django.test import TestCase, override_settings
# from main.models import *
# from main.views import *

# @override_settings(AXES_ENABLED=False)
# class test_login(TestCase):
#     def test_can_access_login_page(self):
#         response = self.client.get("/auth/login")
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'registration/login.html')

#     def test_login(self):
#         response = self.client.post('/auth/login', {'username':'test', 'password': 'test'})
#         self.assertEqual(response.status_code, 200)
    
#     def test_login_success(self):
#         user = CustomUser.objects.create(username='testuser')
#         user.set_password('12345')
#         user.save()
#         response = self.client.login(username='testuser', password='12345')
#         self.assertEqual(response, True)
#         test = self.client.post('/auth/login', {'username':'testuser', 'password': '12345'})
#         self.assertEqual(test.status_code, 302)

