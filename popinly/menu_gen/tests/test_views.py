from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User

from menu_gen.models import Menu, MenuSection, MenuItem

import os
from wand.image import Image


class MenuListViewTests(TestCase):
    def setUp(self):
        """
        Make dummy menus to be used in later tests
        """
        number_of_meuns = 6

        self.username = "jacob"
        self.password = "top_secret"
        self.user = User.objects.create_user(
            username=self.username, email="jacob@test.com", password=self.password
        )

        self.username_two = "jacob_two"
        self.user_two = User.objects.create_user(
            username=self.username_two, email="jacob@test.com", password=self.password
        )

        self.restaurant_name = "Sample Restaurant {}"
        self.menu_title = "Sample Title {}"

        for menu_id in range(number_of_meuns):

            Menu.objects.create(
                menu_title=self.menu_title.format(menu_id),
                restaurant_name=self.restaurant_name.format(menu_id),
                author=self.user,
            )

        # Create a menu for user_two to make sure it doesn't show for user (one)
        Menu.objects.create(
            menu_title=self.menu_title.format(menu_id),
            restaurant_name=self.restaurant_name.format(menu_id),
            author=self.user_two,
        )

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get("/generator/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("menu_gen:index"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("menu_gen:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base_generic.html")
        self.assertTemplateUsed(response, "menu_gen/index.html")

    def test_user_logged_in_as_self(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("menu_gen:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context["user"]), self.username)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("menu_gen:index"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/generator/")

    def test_lists_all_menus(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("menu_gen:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["user_menus"]) == 6)


class MenuExportTests(TestCase):
    def setUp(self):
        """
        Make dummy menus to be used in later tests
        """
        self.username = "jacob"
        self.password = "top_secret"
        self.user = User.objects.create_user(
            username=self.username, email="jacob@test.com", password=self.password
        )

        self.restaurant_name = "Sample Restaurant"
        self.menu_title = "Sample Title"

        self.menu = Menu.objects.create(
            menu_title=self.menu_title,
            restaurant_name=self.restaurant_name,
            author=self.user,
        )

        self.menu_section_dinner = MenuSection.objects.create(
            menu=self.menu,
            name="Dinner",
            description="Tonights Dinner Selection",
            order=2,
        )

        self.menu_section_lunch = MenuSection.objects.create(
            menu=self.menu, name="Lunch", description="Todays Lunch Items", order=1
        )

        MenuItem.objects.create(
            section=self.menu_section_dinner,
            name="spaghetti carbonara",
            description="double smoked bacon, eggs & parmigiano, cream, southern italian style",
            price=16,
            order=1,
        )

        MenuItem.objects.create(
            section=self.menu_section_dinner,
            name="baked ravioli",
            description="cheese or beef ravioli, in arrabiata sauce topped with crispy prosciutto and mozzarella",
            price=18.01,
            order=2,
        )

        MenuItem.objects.create(
            section=self.menu_section_dinner,
            name="tortellini rosé",
            description="ricotta filled pasta, in a rosé sauce",
            price=17.00,
            order=3,
        )

        MenuItem.objects.create(
            section=self.menu_section_lunch,
            name="fettuccine primavera",
            description="cream, fresh vegetables, parmigiano",
            price=0,
            order=1,
        )

    def test_pdf_view_url_exists(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get("/generator/{}/{}".format("pdf", self.menu.uuid))
        self.assertEqual(response.status_code, 200)

    def test_png_view_url_exist(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get("/generator/{}/{}".format("png", self.menu.uuid))
        self.assertEqual(response.status_code, 200)

    def test_pdf_view_url_accessible_by_name(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(
            reverse(
                "menu_gen:detail",
                kwargs={"pk": self.menu.uuid, "export_format": "pdf"},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_png_view_url_accessible_by_name(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(
            reverse(
                "menu_gen:detail",
                kwargs={"pk": self.menu.uuid, "export_format": "png"},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_view_url_inaccessible_by_bad_name(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(
            reverse(
                "menu_gen:detail",
                kwargs={"pk": self.menu.uuid, "export_format": "test123"},
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_pdf_view_uses_correct_template(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(
            reverse(
                "menu_gen:detail",
                kwargs={"pk": self.menu.uuid, "export_format": "pdf"},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "menu_gen/menu_detail.html")

    def test_png_view_uses_correct_template(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(
            reverse(
                "menu_gen:detail",
                kwargs={"pk": self.menu.uuid, "export_format": "png"},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "menu_gen/menu_detail.html")

    def test_pdf_view_returns(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(
            reverse(
                "menu_gen:detail", kwargs={"pk": self.menu.uuid, "export_format": "pdf"}
            )
        )
        self.assertEquals(response.get("Content-Type"), "application/pdf;")

    def test_png_view_returns(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(
            reverse(
                "menu_gen:detail", kwargs={"pk": self.menu.uuid, "export_format": "png"}
            )
        )
        self.assertEquals(response.get("Content-Type"), "image/png;")

    def test_pdf_returned_filename(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(
            reverse(
                "menu_gen:detail", kwargs={"pk": self.menu.uuid, "export_format": "pdf"}
            )
        )
        self.assertEquals(
            response.get("Content-Disposition"),
            "inline; filename={}.pdf".format(self.menu.menu_title),
        )

    def test_png_returned_filename(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(
            reverse(
                "menu_gen:detail", kwargs={"pk": self.menu.uuid, "export_format": "png"}
            )
        )
        self.assertEquals(
            response.get("Content-Disposition"),
            "inline; filename={}.png".format(self.menu.menu_title),
        )

    def test_pdf_matchs_expectated(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(
            reverse(
                "menu_gen:detail", kwargs={"pk": self.menu.uuid, "export_format": "pdf"}
            )
        )
        response_img = Image(blob=response, resolution=150)
        filename = os.path.join(os.path.dirname(__file__), "test_files/sample_pdf.pdf")

        with Image(filename=filename, resolution=150) as expected:
            diff = response_img.compare(expected, metric="root_mean_square")
            self.assertLess(diff[1], 0.01)

    def test_png_matchs_expectated(self):
        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(
            reverse(
                "menu_gen:detail", kwargs={"pk": self.menu.uuid, "export_format": "png"}
            )
        )
        response_img = Image(blob=response, resolution=150)
        filename = os.path.join(os.path.dirname(__file__), "test_files/sample_png.png")

        with Image(filename=filename, resolution=150) as expected:
            diff = response_img.compare(expected, metric="root_mean_square")
            self.assertLess(diff[1], 0.01)
