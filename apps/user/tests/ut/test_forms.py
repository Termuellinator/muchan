from django.test import TestCase

from apps.user.form import UserCreationForm, ModifyUserForm


# class TestUserCreationForm(TestCase):
#     def setUp(self):
#         self.username = "Testuser"
#         self.email = "Test@user.com"
#         self.password = "Testpassword@2023"

#     def test_form_is_valid_for_good_data(self):
#         data = {
#             "username": self.username,
#             "email": self.email,
#             "password1": self.password,
#             "password2": self.password
#         }
        
#         form = UserCreationForm(data=data)
        
#         self.assertTrue(form.is_valid())
        
#     def test_form_not_valid_with_different_pw(self):
#         data = {
#             "username": self.username,
#             "email": self.email,
#             "password1": self.password,
#             "password2": self.password
#         }
        
#         form = UserCreationForm(data=data)
#         # breakpoint()
#         self.assertTrue(form.is_valid())
#         self.assertEqual(form["password2"].errors, 
#                          [str(form.error_messages['password_mismatch'])])
        

class TestModifyUserForm(TestCase):
    def setUp(self):
        self.first_name = "Test"
        self.last_name = "User"
        self.email = "Test@user.com"
        self.title = "Tester"
        self.bio = "Testing is my destiny!"
        
    def test_form_is_valid_for_good_data(self):
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "title": self.title,
            "bio": self.bio
        }
        
        form = ModifyUserForm(data=data)
        
        self.assertTrue(form.is_valid())