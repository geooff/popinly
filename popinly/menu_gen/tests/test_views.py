from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User

from menu_gen.models import Menu, MenuSection, MenuItem


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
        self.user.save()

        self.username_two = "jacob_two"
        self.user_two = User.objects.create_user(
            username=self.username_two, email="jacob@test.com", password=self.password
        )
        self.user_two.save()

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
