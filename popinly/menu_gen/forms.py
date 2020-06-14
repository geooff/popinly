from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, Form, ChoiceField, RadioSelect


from .utils.forms import is_empty_form, is_form_persisted
from .models import Menu, MenuSection, MenuItem

# Adapted from: https://github.com/philgyford/django-nested-inline-formsets-example


class BaseSectionWithItemsFormset(BaseInlineFormSet):
    """
    The base formset for editing menuItems belonging to a menuSections
    """

    def get_queryset(self):
        return super().get_queryset().order_by("order")

    def clean(self):
        """
        Validation to ensure that each menu section is unique
        """
        super().clean()

        orders = []
        for form in self.forms:
            if form.cleaned_data:
                order = form.cleaned_data.get("order", None)
                if order in orders:
                    form.add_error(
                        "order", _("The order of each item in a section must be unique")
                    )
                else:
                    orders.append(order)


# The formset for editing the menuItems that belong to a menuSection.
MenuSectionFormset = inlineformset_factory(
    MenuSection,
    MenuItem,
    formset=BaseSectionWithItemsFormset,
    fields=("name", "description", "price", "order"),
    extra=1,
    can_order=False,
    can_delete=True,
    labels={
        "name": _("Item Name"),
        "description": _("Item Description"),
        "price": _("Item Price"),
    },
)


class BaseMenuWithSectionFormset(BaseInlineFormSet):
    """
    The base formset for editing menuSections belonging to a Menu
    """

    def get_queryset(self):
        return super().get_queryset().order_by("order")

    def add_fields(self, form, index):
        super().add_fields(form, index)

        # Save the formset for a Menus's Items in the nested property.
        form.nested = MenuSectionFormset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix="menuitem-%s-%s"
            % (form.prefix, MenuSectionFormset.get_default_prefix()),
        )

    def is_valid(self):
        """
        Also validate the nested formsets.
        """
        result = super().is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, "nested"):
                    result = result and form.nested.is_valid()

        return result

    def clean(self):
        """
        If a parent form has no data, but its nested forms do, we should
        return an error, because we can't save the parent.
        For example, if the menuSection form is empty, but there are menuItems.
        """
        super().clean()

        orders = []
        for form in self.forms:
            if not hasattr(form, "nested") or self._should_delete_form(form):
                continue

            if self._is_adding_nested_inlines_to_empty_form(form):
                form.add_error(
                    field=None,
                    error=_(
                        "You are trying to add menu items(s) to a menu section which "
                        "does not yet exist. Please add information "
                        "about the menu section and try again."
                    ),
                )

            # Validation to ensure that each menu section is unique
            if form.cleaned_data:
                order = form.cleaned_data.get("order", None)
                if order in orders:
                    form.add_error(
                        "Order",
                        _("The order of each section in the menu must be unique"),
                    )
                else:
                    orders.append(order)

    def save(self, commit=True):
        """
        Also save the nested formsets.
        """
        result = super().save(commit=commit)

        for form in self.forms:
            if hasattr(form, "nested"):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result

    def _is_adding_nested_inlines_to_empty_form(self, form):
        """
        Are we trying to add data in nested inlines to a form that has no data?
        e.g. Adding menuItems to a new menuSection whose data we haven't entered?
        """
        if not hasattr(form, "nested"):
            # A basic form; it has no nested forms to check.
            return False

        if is_form_persisted(form):
            # We're editing (not adding) an existing model.
            return False

        if not is_empty_form(form):
            # The form has errors, or it contains valid data.
            return False

        # All the inline forms that aren't being deleted:
        non_deleted_forms = set(form.nested.forms).difference(
            set(form.nested.deleted_forms)
        )

        # At this point we know that the "form" is empty.
        # In all the inline forms that aren't being deleted, are there any that
        # contain data? Return True if so.
        return any(not is_empty_form(nested_form) for nested_form in non_deleted_forms)


# This is the formset for the menuSections belonging to a Menu and the
# menuItems belonging to those menuSections.
MenuSectionsItemsFormset = inlineformset_factory(
    Menu,
    MenuSection,
    formset=BaseMenuWithSectionFormset,
    fields=("name", "description", "order"),
    extra=1,
    can_order=False,
    can_delete=True,
    labels={"name": _("Section Name"), "description": _("Section Description")},
)


class WizardRestaurantForm(ModelForm):
    class Meta:
        model = Menu
        fields = ["restaurant_name", "menu_title"]


class WizardStyleForm(ModelForm):
    class Meta:
        model = Menu
        fields = ["colour_palette", "title_font", "base_font"]


class WizardMenuTypeForm(ModelForm):
    class Meta:
        model = Menu
        fields = ["menu_type"]
        widgets = {
            "menu_type": RadioSelect(),
        }
