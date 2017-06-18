from django import forms

from animal.models import Animal, AnimalType, Activity


class ModelChoiceFieldWithEmptyLabel(forms.ModelChoiceField):

    def __init__(self, *args, **kwargs):
        empty_label = kwargs.get("empty_label")
        super().__init__(*args, **kwargs)
        if empty_label:
            self.empty_label = empty_label


class TypedChoiceFieldNoValidation(forms.TypedChoiceField):
    def clean(self, value):
        return self._coerce(value)

    def validate(self, value):
        pass


class Form1(forms.ModelForm):

    class Meta:
        model = Animal
        fields = ["name", "age", "type", "favorite_activity", "activities"]


class DynamicRequired1(forms.ModelForm):
    """Required is checked in clean().
    Also add an empty label to a required model choicefield.
    """

    type = ModelChoiceFieldWithEmptyLabel(
        queryset=AnimalType.objects.all(),
        empty_label='Select Animal Type')

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
    """Required attribute is changed in __init__
    """

    type = ModelChoiceFieldWithEmptyLabel(
        queryset=AnimalType.objects.all(),
        empty_label='Select Animal Type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        animal_type = self.data.get("type")
        if animal_type == "cat":
            self.fields["age"].required = True

    class Meta:
        model = Animal
        fields = ["name", "age", "type", "favorite_activity", "activities"]


def get_animal_type(value):
    return AnimalType(pk=value)


def get_activity(value):
    return Activity.objects.get(pk=value)


class DynamicRequired3(forms.ModelForm):
    """Alternative to model choice field
    """

    type = forms.TypedChoiceField(
        empty_value=None,  # Value given to empty choice
        coerce=get_animal_type,
        required=True)

    favorite_activity = TypedChoiceFieldNoValidation(
        empty_value=None,  # Value given to empty choice
        coerce=get_activity,
        required=True)

    age = forms.TypedChoiceField(
        required=False,
        empty_value=None,
        coerce=int,
        choices=[("", "Select Age"), ("1", "1"), ("2", "2")])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        choices = [
            (type.pk, type.label)
            for type in AnimalType.objects.all()]
        choices.insert(0, ("", "Select an animal"))
        self.fields["type"].choices = choices

    def clean(self):
        cleaned_data = super().clean()
        activity = cleaned_data.get("favorite_activity")
        type = cleaned_data.get("type")
        if activity and type and activity.animal_type_id != type.pk:
            self.add_error("favorite_activity", "Not a valid activity")

    class Meta:
        model = Animal
        fields = ["name", "age", "type", "favorite_activity", "activities"]


# TODO
# DynamicRequired4: Set choices depending on type in init
# Multi select with hack for pk...
# Add a weird choice in type (Tiger, use internal notes)
# BasicForm: form with initial and save!
