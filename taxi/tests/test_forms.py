from django.contrib.auth import get_user_model
from django.forms import CheckboxSelectMultiple
from django.test import TestCase

from taxi.forms import (
    ManufacturerSearchForm,
    CarForm,
    CarSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
)
from taxi.models import Manufacturer


class ManufacturerFormsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.search_form_data = {
            "name": "test",
        }

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data=self.search_form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.search_form_data)

    def test_manufacturer_search_form_placeholder_text(self):
        form = ManufacturerSearchForm(data=self.search_form_data)
        expected_text = "Search by manufacturer"
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"],
            expected_text
        )


class CarFormsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="user1_username",
            password="test12password"
        )
        Manufacturer.objects.create(
            name="manufacturer1_name",
            country="manufacturer1_country",
        )
        cls.form_data = {
            "model": "test_model",
            "manufacturer": Manufacturer.objects.first(),
            "drivers": get_user_model().objects.all(),
        }
        cls.search_form_data = {
            "model": "test_model",
        }

    def test_car_form(self):
        form = CarForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], self.form_data["model"])
        self.assertEqual(
            form.cleaned_data["manufacturer"],
            self.form_data["manufacturer"]
        )
        self.assertEqual(
            list(form.cleaned_data["drivers"]),
            list(self.form_data["drivers"])
        )

    def test_car_form_uses_checkboxes_for_drivers_field(self):
        form = CarForm(data=self.form_data)
        self.assertTrue(
            isinstance(form.fields["drivers"].widget, CheckboxSelectMultiple)
        )

    def test_car_search_form(self):
        form = CarSearchForm(data=self.search_form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.search_form_data)

    def test_car_search_form_placeholder_text(self):
        form = CarSearchForm(data=self.search_form_data)
        expected_text = "Search by model"
        self.assertEqual(
            form.fields["model"].widget.attrs["placeholder"],
            expected_text
        )


class DriverFormsTest(TestCase):
    def setUp(self):
        self.creation_form_data = {
            "username": "user1_username",
            "first_name": "user1_fname",
            "last_name": "user1_lname",
            "license_number": "QWE12345",
            "password1": "test12password",
            "password2": "test12password",
        }
        self.license_form_data = {
            "license_number": "QWE12345",
        }
        self.search_form_data = {
            "username": "user1_username",
        }
        self.invalid_license_numbers = [
            "QWE1234",
            "qWE12345",
            "QWE1234r",
            "QW123456"
        ]

    def test_driver_creation_form(self):
        form = DriverCreationForm(data=self.creation_form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.creation_form_data)

    def test_driver_creation_form_with_invalid_license_number(self):
        for invalid_license_number in self.invalid_license_numbers:
            self.creation_form_data["license_number"] = invalid_license_number
            form = DriverCreationForm(data=self.creation_form_data)
            self.assertFalse(form.is_valid())

    def test_driver_license_update_form(self):
        form = DriverLicenseUpdateForm(data=self.license_form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.license_form_data)

    def test_driver_license_update_form_with_invalid_license_number(self):
        for invalid_license_number in self.invalid_license_numbers:
            self.license_form_data["license_number"] = invalid_license_number
            form = DriverLicenseUpdateForm(data=self.license_form_data)
            self.assertFalse(form.is_valid())

    def test_driver_search_form(self):
        form = DriverSearchForm(data=self.search_form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.search_form_data)

    def test_driver_search_form_placeholder_text(self):
        form = DriverSearchForm(data=self.search_form_data)
        expected_text = "Search by username"
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"],
            expected_text
        )
