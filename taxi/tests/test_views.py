from django.contrib.auth import get_user_model, get_user
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer


USER_DATA = {
    "username": "user1_username",
    "first_name": "user1_fname",
    "last_name": "user1_lname",
    "license_number": "QWE12345",
    "password": "test12password",
}


class PublicViewsTest(TestCase):
    def test_redirect_if_not_logged_in(self):
        paths = [
            "/",
            "/cars/",
            "/drivers/",
            "/manufacturers/",
        ]
        for path in paths:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, f"/accounts/login/?next={path}")


class UserAuthTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(**USER_DATA)
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.index_url = reverse("taxi:index")

    def test_user_login(self):
        response = self.client.post(
            self.login_url,
            {
                "username": USER_DATA["username"],
                "password": USER_DATA["password"]
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)
        user = get_user(self.client)
        self.assertEqual(user, self.user)


class PrivateManufacturerViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_manufacturers = 24
        for i in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name=f'test_manufacturer{i}',
                country=f"test_country{i}",
            )

    def setUp(self):
        self.user = get_user_model().objects.create_user(**USER_DATA)
        self.client.force_login(self.user)
        self.manufacturer_list_url = reverse("taxi:manufacturer-list")

    def test_logged_in_uses_correct_template(self):
        response = self.client.get(self.manufacturer_list_url)
        self.assertEqual(
            str(response.context["user"]),
            "user1_username (user1_fname user1_lname)"
        )
        self.assertTemplateUsed(
            response,
            template_name="taxi/manufacturer_list.html"
        )

    def test_pagination_is_five(self):
        response = self.client.get(self.manufacturer_list_url)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_list_all_manufacturers(self):
        response = self.client.get(self.manufacturer_list_url + "?page=5")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 4)

    def test_manufacturer_search_returns_correct_amount_of_items(self):
        response = self.client.get(
            self.manufacturer_list_url,
            {
                "name": 2,
                "page": 2

            }
        )
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
