import datetime

from django.test import TestCase, Client
from django.utils import timezone

from django.contrib.auth.models import User


class TestIndexView(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_index_response(self):
        # Issue a GET request.
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


class TestSignupView(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_index_response(self):
        # Issue a GET request.
        response = self.client.get("/signup/")
        self.assertEqual(response.status_code, 200)


class TestLoginView(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_index_response(self):
        # Issue a GET request.
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)


class TestPasswordResetView(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_index_response(self):
        # Issue a GET request.
        response = self.client.get("/accounts/password_reset/")
        self.assertEqual(response.status_code, 200)
