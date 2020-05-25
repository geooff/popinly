import datetime

from django.test import TestCase
from django.utils import timezone

from django.contrib.auth.models import User


from .models import Menu, MenuSection, MenuItem


class MenuModelTests(TestCase):
    # Test cases for the Menu Model
    def setUp(self):
        """
        Make a dummy menu to be used in later tests
        """
        self.user = User.objects.create_user(
            username="jacob", email="jacob@test.com", password="top_secret"
        )

        self.restaurant_name = "Sample Restaurant"
        self.menu_title = "Sample Title"
        self.menu = Menu.objects.create(
            menu_title=self.menu_title,
            restaurant_name=self.restaurant_name,
            author=self.user,
        )

    def test_menu_owner(self):
        """
        test that creator of menu owns the menu
        """
        self.assertIs(self.menu.author, self.user)

    def test_menu_naming(self):
        """
        test creating a menu.
        """
        self.assertIs(self.menu.__str__(), self.menu_title)


class SectionModelTests(TestCase):
    # Test cases for the MenuSection Model
    def setUp(self):
        """
        Make a dummy menu to be used in later tests
        """
        self.user = User.objects.create_user(
            username="jacob", email="jacob@test.com", password="top_secret"
        )

        restaurant_name = "Sample Restaurant"
        menu_title = "Sample Title"
        self.menu = Menu.objects.create(
            menu_title=menu_title, restaurant_name=restaurant_name, author=self.user
        )

        self.section_name = "Sample Section"
        self.order = 1
        self.section = MenuSection(
            name=self.section_name, order=self.order, menu=self.menu
        )

        self.another_section_name = "Second Section"
        self.another_order = 2
        self.another_section = MenuSection(
            name=self.another_section_name, order=self.another_order, menu=self.menu
        )

        # Calling save required when doing work with query_set
        self.another_section.save()
        self.section.save()
        self.menu.save()

    def test_section_naming(self):
        """
        test creating a menu section.
        """
        self.assertIs(self.section.__str__(), self.section_name)

    def test_section_parent(self):
        """
        test that the sections owner is its parent menu
        """
        self.assertIs(self.section.menu, self.menu)

    def test_section_relationship(self):
        """
        test that multiple sections can belong to a parent
        """
        self.assertIs(self.menu.menusection_set.count(), 2)

    def test_section_ordering(self):
        """
        test that multiple sections order properly
        """
        index_order = self.another_order - 1
        section = self.menu.menusection_set.all()[index_order]
        self.assertEqual(
            getattr(section, "name"), self.another_section_name,
        )


class ItemModelTests(TestCase):
    # Test cases for the MenuSection Model
    def setUp(self):
        """
        Make a dummy menu to be used in later tests
        """
        self.user = User.objects.create_user(
            username="jacob", email="jacob@test.com", password="top_secret"
        )

        restaurant_name = "Sample Restaurant"
        menu_title = "Sample Title"
        self.menu = Menu.objects.create(
            menu_title=menu_title, restaurant_name=restaurant_name, author=self.user
        )

        self.section_name = "Sample Section"
        self.order = 1
        self.section = MenuSection(
            name=self.section_name, order=self.order, menu=self.menu
        )

        self.another_section_name = "Second Section"
        self.another_order = 2
        self.another_section = MenuSection(
            name=self.another_section_name, order=self.another_order, menu=self.menu
        )

        self.item_name = "Swagetti"
        self.item_price = 12.12
        self.item_order = 1
        self.item = MenuItem(
            section=self.section,
            name=self.item_name,
            price=self.item_price,
            order=self.item_order,
        )

        self.another_item_name = "Swagetti 2"
        self.another_item_price = 21.12
        self.another_item_order = 2
        self.another_item = MenuItem(
            section=self.section,
            name=self.another_item_name,
            price=self.another_item_price,
            order=self.another_item_order,
        )

        # Calling save required when doing work with query_set
        self.another_item.save()
        self.item.save()
        self.another_section.save()
        self.section.save()
        self.menu.save()

    def test_item_naming(self):
        """
        test creating a menu section.
        """
        self.assertIs(self.item.__str__(), self.item_name)

    def test_item_parent(self):
        """
        test that the item owner is its parent section
        """
        self.assertIs(self.item.section, self.section)

    def test_item_relationship(self):
        """
        test that multiple items can belong to a parent section
        """
        self.assertIs(self.section.menuitem_set.count(), 2)

    def test_section_ordering(self):
        """
        test that multiple items order properly
        """
        index_order = self.another_item_order - 1
        section = self.section.menuitem_set.all()[index_order]
        self.assertEqual(
            getattr(section, "name"), self.another_item_name,
        )

    def test_whole_tree(self):
        ordered_tree = list()
        for section in self.menu.menusection_set.all():
            ordered_tree.append(section)
            for item in section.menuitem_set.all():
                ordered_tree.append(item)

        # This order is hard coded to test the order logic more
        expected = [self.section, self.item, self.another_item, self.another_section]
        self.assertEqual(ordered_tree, expected)
