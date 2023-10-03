from django.test import TestCase, override_settings

from apps.user.form import RegisterUserForm, ModifyUserForm
from apps.user.models import User


class TestRegisterUserForm(TestCase):
    def setUp(self):
        self.username = "Testuser"
        self.email = "Test@user.com"
        self.password = "Testpassword@2023"

    def test_form_is_valid_for_good_data(self):
        data = {
            "username": self.username,
            "email": self.email,
            "password1": self.password,
            "password2": self.password
        }

        form = RegisterUserForm(data=data)

        self.assertTrue(form.is_valid())

    def test_form_not_valid_with_different_pw(self):
        data = {
            "username": self.username,
            "email": self.email,
            "password1": self.password,
            "password2": self.password + "123"
        }

        form = RegisterUserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form["password2"].errors,
                         [str(form.error_messages['password_mismatch'])])

    def test_form_valid_with_unicode_username(self):
        data = {
            "username": "宝",
            "email": self.email,
            "password1": self.password,
            "password2": self.password
        }
        form = RegisterUserForm(data=data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "宝")
        
    def test_duplicate_normalized_unicode(self):
        """To prevent almost identical usernames, visually identical but 
        differing by their unicode code points only, Unicode NFKC 
        normalization should make appear them equal to Django.
        """
        omega_username = "iamtheΩ"  # U+03A9 GREEK CAPITAL LETTER OMEGA
        ohm_username = "iamtheΩ"  # U+2126 OHM SIGN
        self.assertNotEqual(omega_username, ohm_username)
        User.objects.create_user(username=omega_username, password='pwd')
        data = {
            "username": ohm_username,
            "email": self.email,
            "password1": self.password,
            "password2": self.password
        }
        form = RegisterUserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["username"], 
            ["A user with that username already exists."]
        )

    @override_settings(AUTH_PASSWORD_VALIDATORS=[
        {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", 
         "OPTIONS": {"min_length": 10,}},
        ])
    def test_form_invalid_if_password_like_username(self):
        data = {
            "username": self.username,
            "password1": self.username,
            "password2": self.username,
        }
        form = RegisterUserForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form["password2"].errors), 2)
        self.assertIn("The password is too similar to the username.", 
                      form["password2"].errors)
        self.assertIn(
            "This password is too short. It must contain at least 10 characters.",
            form["password2"].errors
        )

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

    def test_form_is_invalid_for_bad_email(self):
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": "notanemail",
            "title": self.title,
            "bio": self.bio
        }

        form = ModifyUserForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["email"], ["Enter a valid email address."]
        )
