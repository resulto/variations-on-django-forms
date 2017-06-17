from django import forms

from animal.models import Animal, AnimalType


class ModelChoiceFieldWithEmptyLabel(forms.ModelChoiceField):

    def __init__(self, *args, **kwargs):
        empty_label = kwargs.get("empty_label")
        super().__init__(*args, **kwargs)
        if empty_label:
            self.empty_label = empty_label


class Form1(forms.ModelForm):

    class Meta:
        model = Animal
        fields = ["name", "age", "type", "favorite_activity", "activities"]


class DynamicRequired1(forms.ModelForm):

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
