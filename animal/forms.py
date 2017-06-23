from typing import TypeVar, List

from django import forms
from django.db import models

from animal.models import Animal, AnimalType, Activity


M = TypeVar('M', bound=models.Model)      # Declare type variable


def materialize_models(models: List[M]) -> List[M]:
    """Retrieves a list of models from the DB if the models did not come from a
    DB. This is useful if:

    1. You want to add the models to a m2m relationship
    2. The models were constructed like Model(pk=pk)
    """
    if not models:
        return models

    obj = models[0]

    if not obj._state.db:
        pks = [model.pk for model in models]
        Model = obj._meta.model

        return list(Model.objects.filter(pk__in=pks))
    else:
        return models


class ModelChoiceFieldWithEmptyLabel(forms.ModelChoiceField):
    """Adds an empty label to the choice even if the field is required.
    """

    def __init__(self, *args, **kwargs):
        empty_label = kwargs.get("empty_label")
        super().__init__(*args, **kwargs)
        if empty_label:
            self.empty_label = empty_label


class TypedChoiceFieldNoValidation(forms.TypedChoiceField):
    """Does not validate the selected value in a list of choices.

    Effectively delegates validation to the coerce function and clean function.
    """

    def clean(self, value):
        return self._coerce(value)

    def validate(self, value):
        pass


class TypedMultipleChoiceFieldNoValidation(forms.TypedMultipleChoiceField):
    """Does not validate the selected value in a list of choices.

    Effectively delegates validation to the coerce function and clean function.
    """

    def clean(self, value):
        return self._coerce(value)

    def validate(self, value):
        pass


class Form1(forms.ModelForm):
    """Basic ModelForm
    """

    class Meta:
        model = Animal
        fields = ["name", "age", "type", "favorite_activity", "activities"]


class DynamicRequired1(forms.ModelForm):
    """
    Age required if type is cat. This is checked in clean().

    Adding an empty label, e.g., 'Please select this' to a modelchoicefield can
    be tricky and is best done with subclassing or by setting empty_label
    explicitly after the form's __init__.
    """

    type = ModelChoiceFieldWithEmptyLabel(
        queryset=AnimalType.objects.all(),
        empty_label='Select Animal Type')
    """Subclass to add an empty label in all cases even when there is a default
    value."""

    def clean(self):
        cleaned_data = super().clean()
        animal_type = cleaned_data.get("type")
        if animal_type and animal_type.pk == "cat":
            if cleaned_data.get("age") is None:
                self.add_error("age", "Age is required when cat is selected")

    class Meta:
        model = Animal
        fields = ["name", "age", "type", "favorite_activity", "activities"]


class DynamicRequired2(forms.ModelForm):
    """
    Age is required if type is cat. This time, we set the required attribute in
    __init__. The required validation is more standard BUT we must work with
    unvalidated data instead of cleaned_data.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Alternative to ModelChoiceFieldWithEmptyLabel
        self.fields["type"].empty_label = "Select Animal Type"
        animal_type = self.data.get(self.add_prefix("type"))
        if animal_type == "cat":
            self.fields["age"].required = True

    class Meta:
        model = Animal
        fields = ["name", "age", "type", "favorite_activity", "activities"]


def get_animal_type(value):
    """Demonstrates the lazy hack: no fetch to DB. Do think only if you are
    100% sure that value is a valid pk.

    Do not use this if you need to access AnimalType fields.
    """
    # Not called when value is empty
    return AnimalType(pk=value)


def get_activity(value):
    """Fetches the activity from the DB.
    """
    # Not called when value is empty
    try:
        return Activity.objects.get(pk=value)
    except Activity.DoesNotExist:
        # Will add a standard invalid choice error.
        raise forms.ValidationError()


def get_lazy_activity(value):
    """Demonstrates the lazy hack: no fetch to DB. Do think only if you are
    100% sure that value is a valid pk.

    Do not use this if you need to access AnimalType fields.
    """
    # Not called when value is empty
    return Activity(pk=value)


class DynamicRequired3(forms.ModelForm):
    """
    Demonstrates the use of TypedChoiceField to replace a ModelChoiceField.
    """

    type = forms.TypedChoiceField(
        empty_value=None,  # Value given to empty choice
        coerce=get_animal_type,
        required=True)

    favorite_activity = TypedChoiceFieldNoValidation(
        empty_value=None,  # Value given to empty choice
        coerce=get_activity,
        required=True)
    """Will not validate the value with a list of choices"""

    age = forms.TypedChoiceField(
        required=False,
        # Try to remove empty_value and see what happens if you do not
        # enter anything.
        empty_value=None,
        coerce=int,
        choices=[("", "Select Age"), ("1", "1"), ("2", "2")])
    """You can transform a standard field into a choice field."""

    activities = forms.TypedMultipleChoiceField(
        empty_value=None,  # Value given to empty choice
        coerce=get_lazy_activity,
        required=True)
    """Will validate the value with a list of choices defined
    in __init__"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # XXX Example how we can build a completely custom list of choices
        # for a FK in a model.
        choices = [
            (type.pk, type.label)
            for type in AnimalType.objects.all()]
        choices.insert(0, ("", "Select an animal"))
        self.fields["type"].choices = choices

        # XXX Set activity choices for this animal type.
        animal_type = self.data.get(self.add_prefix("type"))
        if animal_type:
            choices = [
                (activity.pk, activity.label) for activity in
                Activity.objects.filter(animal_type_id=animal_type)
            ]
            self.fields["activities"].choices = choices

    def clean(self):
        cleaned_data = super().clean()
        activity = cleaned_data.get("favorite_activity")
        type = cleaned_data.get("type")

        if activity and type and activity.animal_type_id != type.pk:
            self.add_error("favorite_activity", "Not a valid activity")

    def save(self, *args, **kwargs):
        # XXX With m2m, lazy objects do not work :-(
        # Imagine if your list has thousands of choices and the user
        # can select hundreds of choice. This method has very good performance,
        # but it offers no validation (hence the choice computation in
        # __init__).
        activities = self.cleaned_data.get("activities")
        if activities:
            new_activities = materialize_models(activities)
            self.cleaned_data["activities"] = new_activities
        super().save(*args, **kwargs)

    class Meta:
        model = Animal
        fields = ["name", "age", "type", "favorite_activity", "activities"]


class DynamicRequired4(forms.Form):
    """Replaces a ModelForm by a form when you have heavily customized fields.
    """

    name = forms.CharField(
        label="name")
    age = forms.IntegerField(
        label="age", required=False)
    type = forms.ChoiceField(
        label="Type")
    favorite_activity = forms.TypedChoiceField(
        coerce=int,
        empty_value=None,
        label="Favorite Activity")
    activities = forms.TypedMultipleChoiceField(
        coerce=int,
        empty_value=None,
        label="Activities")

    def __init__(self, *args, **kwargs):
        # Instance is not a valid keyword arg so we remove it
        instance = kwargs.pop("instance", None)
        if instance:
            initial = self.get_initial(instance)
            kwargs["initial"] = initial
            print(kwargs)
        super().__init__(*args, **kwargs)

        choices = [
            (type.pk, type.label)
            for type in AnimalType.objects.all()]
        choices.insert(0, ("", "Select an animal"))
        choices.append(("tiger", "Tiger"))
        self.fields["type"].choices = choices

        choices = [
            (activity.pk, activity.label)
            for activity in Activity.objects.all()
        ]
        choices.insert(0, ("", "Select an activity"))
        self.fields["favorite_activity"].choices = choices
        new_choices = choices[1:]
        self.fields["activities"].choices = new_choices

    def get_initial(self, instance):
        initial = {
            "name": instance.name,
            "age": instance.age,
            "type": instance.type_id,
            "favorite_activity": instance.favorite_activity_id,
            "activities": [
                activity.pk for activity in instance.activities.all()]
        }
        if instance.internal_notes == "tiger":
            initial["type"] = "tiger"
        return initial

    def save_instance(self):
        type = self.cleaned_data["type"]
        if type == "tiger":
            internal_notes = "tiger"
            type = AnimalType(pk="cat")
        else:
            internal_notes = ""

        animal = Animal(
            type=type,
            age=self.cleaned_data["age"],
            name=self.cleaned_data["name"],
            favorite_activity=Activity(
                pk=self.cleaned_data["favorite_activity"]),
            internal_notes=internal_notes
        )
        animal.save()
        activities = Activity.objects.filter(
            pk__in=self.cleaned_data["activities"])
        animal.activities.add(*activities)
