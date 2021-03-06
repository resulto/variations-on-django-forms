import json

from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse

from animal import forms
from animal.models import Animal, Activity, AnimalType


def get_menu_items():
    return [
        {
            "page_name": "home",
            "url": reverse("animal:home"),
            "title": "Model Form",
        }, {
            "page_name": "dynamic1",
            "url": reverse("animal:dynamic_required_1"),
            "title": "Dynamic Required 1",
        }, {
            "page_name": "dynamic2",
            "url": reverse("animal:dynamic_required_2"),
            "title": "Dynamic Required 2",
        }, {
            "page_name": "dynamic3",
            "url": reverse("animal:dynamic_required_3"),
            "title": "Dynamic Required 3",
        }, {
            "page_name": "dynamic4",
            "url": reverse("animal:dynamic_required_4"),
            "title": "Dynamic Required 4",
        },
    ]


class AnimalView(View):

    page_name = ""

    def __init__(self):
        super().__init__()
        self.context = {}
        self.context["page_name"] = self.page_name
        self.context["menu_items"] = get_menu_items()

    def _add_form_context(self, form):
        form_types = [
            {
                "value": choice[0],
                "label": choice[1]
            } for choice in form.fields["type"].choices
        ]
        form_activities = [
            {
                "value": choice[0],
                "label": choice[1]
            } for choice in form.fields["favorite_activity"].choices
        ]
        self.context.update({
            "form": form,
            "form_types_json": json.dumps(form_types),
            "form_activities_json": json.dumps(form_activities),
        })

    def dispatch(self, request, *args, **kwargs):
        activities = [
            {
                "value": activity.pk,
                "label": activity.label,
                "for_type": activity.animal_type.pk
            } for activity in Activity.objects.all()
        ]
        types = [
            {
                "value": type.pk,
                "label": type.label
            } for type in AnimalType.objects.all()
        ]
        types.insert(0, {
            "value": "",
            "label": "Select animal type"
        })
        self.context.update({
            "animals": Animal.objects.order_by("pk"),
            "activities_json": json.dumps(activities),
            "types_json": json.dumps(types),
        })
        return super().dispatch(request, *args, **kwargs)


class Home(AnimalView):

    page_name = "home"
    template_file = "animal/home.html"

    def get(self, request):
        self.context.update({
            "success": request.GET.get("success") == "success",
        })
        self._add_form_context(forms.Form1())
        return render(request, self.template_file, self.context)

    def post(self, request):
        form = forms.Form1(data=request.POST)
        if form.is_valid():
            form.save()
            url = reverse("animal:home") + "?success=success"
            return redirect(url)
        else:
            self.context.update({"success": False})
            self._add_form_context(form)
            return render(request, self.template_file, self.context)


class DynamicRequired1(AnimalView):

    page_name = "dynamic1"
    template_file = "animal/dynamic_required_1.html"

    def get(self, request):
        self.context.update({
            "success": request.GET.get("success") == "success",
        })
        self._add_form_context(forms.DynamicRequired1())
        return render(request, self.template_file, self.context)

    def post(self, request):
        form = forms.DynamicRequired1(data=request.POST)
        if form.is_valid():
            form.save()
            url = reverse("animal:dynamic_required_1") + "?success=success"
            return redirect(url)
        else:
            self.context.update({"success": False})
            self._add_form_context(form)
            return render(request, self.template_file, self.context)


class DynamicRequired2(AnimalView):

    page_name = "dynamic2"
    template_file = "animal/dynamic_required_2.html"

    def get(self, request):
        self.context.update({
            "success": request.GET.get("success") == "success",
        })
        self._add_form_context(forms.DynamicRequired2())
        return render(request, self.template_file, self.context)

    def post(self, request):
        form = forms.DynamicRequired2(data=request.POST)
        if form.is_valid():
            form.save()
            url = reverse("animal:dynamic_required_2") + "?success=success"
            return redirect(url)
        else:
            self.context.update({"success": False})
            self._add_form_context(form)
            return render(request, self.template_file, self.context)


class DynamicRequired3(AnimalView):

    page_name = "dynamic3"
    template_file = "animal/dynamic_required_3.html"

    def get(self, request):
        self.context.update({
            "success": request.GET.get("success") == "success",
        })
        self._add_form_context(forms.DynamicRequired3())
        self._add_age_choices()
        return render(request, self.template_file, self.context)

    def post(self, request):
        form = forms.DynamicRequired3(data=request.POST)
        if form.is_valid():
            form.save()
            url = reverse("animal:dynamic_required_3") + "?success=success"
            return redirect(url)
        else:
            self.context.update({"success": False})
            self._add_form_context(form)
            self._add_age_choices()
            return render(request, self.template_file, self.context)

    def _add_age_choices(self):
        form = self.context["form"]
        age_choices = [
            {
                "value": choice[0],
                "label": choice[1]
            } for choice in form.fields["age"].choices]
        self.context["form_age_json"] = json.dumps(age_choices)


class DynamicRequired4(AnimalView):

    page_name = "dynamic4"
    template_file = "animal/dynamic_required_4.html"

    def get(self, request):
        # animal = Animal.objects.order_by("-pk").first()
        # form = forms.DynamicRequired4(instance=animal)
        form = forms.DynamicRequired4()
        self.context.update({
            "success": request.GET.get("success") == "success",
            "form": form,
        })
        return render(request, self.template_file, self.context)

    def post(self, request):
        form = forms.DynamicRequired4(data=request.POST)
        if form.is_valid():
            # Notice the custom method!
            form.save_instance()
            url = reverse("animal:dynamic_required_4") + "?success=success"
            return redirect(url)
        else:
            self.context.update({
                "success": False,
                "form": form
            })
            return render(request, self.template_file, self.context)
