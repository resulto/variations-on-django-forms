import json

from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse

from animal import forms
from animal.models import Animal, Activity, AnimalType


class AnimalView(View):

    def _fill_context(self, context):
        form = context["form"]
        form_types = [
            {
                "value": choice[0],
                "label": choice[1]
            } for choice in form.fields["type"].choices
        ]
        context["form_types_json"] = json.dumps(form_types)

        form_activities = [
            {
                "value": choice[0],
                "label": choice[1]
            } for choice in form.fields["favorite_activity"].choices
        ]
        context["form_activities_json"] = json.dumps(form_activities)

    def dispatch(self, request, *args, **kwargs):
        self.context = {}
        self.context["animals"] = Animal.objects.order_by("pk")
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
        self.context["activities_json"] = json.dumps(activities)
        self.context["types_json"] = json.dumps(types)
        return super().dispatch(request, *args, **kwargs)


class Home(AnimalView):

    def get(self, request):
        context = self.context
        template_name = "animal/home.html"
        context["success"] = request.GET.get("success") == "success"
        context["form"] = forms.Form1()
        self._fill_context(context)
        return render(request, template_name, context)

    def post(self, request):
        context = self.context
        template_name = "animal/home.html"
        form = forms.Form1(data=request.POST)
        if form.is_valid():
            form.save()
            url = reverse("animal:home") + "?success=success"
            return redirect(url)
        else:
            context["form"] = form
            context["success"] = False
            self._fill_context(context)
            template_name = "animal/home.html"
            return render(request, template_name, context)


class DynamicRequired1(AnimalView):

    def get(self, request):
        context = self.context
        template_name = "animal/dynamic_required_1.html"
        context["success"] = request.GET.get("success") == "success"
        context["form"] = forms.DynamicRequired1()
        self._fill_context(context)
        return render(request, template_name, context)

    def post(self, request):
        context = self.context
        template_name = "animal/dynamic_required_1.html"
        form = forms.DynamicRequired1(data=request.POST)
        if form.is_valid():
            form.save()
            url = reverse("animal:dynamic_required_1") + "?success=success"
            return redirect(url)
        else:
            context["form"] = form
            context["success"] = False
            self._fill_context(context)
            template_name = "animal/dynamic_required_1.html"
            return render(request, template_name, context)


class DynamicRequired2(AnimalView):

    def get(self, request):
        context = self.context
        template_name = "animal/dynamic_required_2.html"
        context["success"] = request.GET.get("success") == "success"
        context["form"] = forms.DynamicRequired2()
        self._fill_context(context)
        return render(request, template_name, context)

    def post(self, request):
        context = self.context
        template_name = "animal/dynamic_required_2.html"
        form = forms.DynamicRequired2(data=request.POST)
        if form.is_valid():
            form.save()
            url = reverse("animal:dynamic_required_2") + "?success=success"
            return redirect(url)
        else:
            context["form"] = form
            context["success"] = False
            self._fill_context(context)
            template_name = "animal/dynamic_required_2.html"
            return render(request, template_name, context)


class DynamicRequired3(AnimalView):

    def get(self, request):
        context = self.context
        template_name = "animal/dynamic_required_3.html"
        context["success"] = request.GET.get("success") == "success"
        context["form"] = forms.DynamicRequired3()
        self._fill_context(context)
        self._add_age_choices(context)
        return render(request, template_name, context)

    def post(self, request):
        context = self.context
        template_name = "animal/dynamic_required_3.html"
        form = forms.DynamicRequired3(data=request.POST)
        if form.is_valid():
            form.save()
            url = reverse("animal:dynamic_required_3") + "?success=success"
            return redirect(url)
        else:
            context["form"] = form
            context["success"] = False
            self._fill_context(context)
            self._add_age_choices(context)
            template_name = "animal/dynamic_required_3.html"
            return render(request, template_name, context)

    def _add_age_choices(self, context):
        form = context["form"]
        age_choices = [
            {
                "value": choice[0],
                "label": choice[1]
            } for choice in form.fields["age"].choices]
        context["form_age_json"] = json.dumps(age_choices)


class DynamicRequired4(AnimalView):

    def get(self, request):
        context = self.context
        template_name = "animal/dynamic_required_4.html"
        context["success"] = request.GET.get("success") == "success"
        # animal = Animal.objects.order_by("-pk").first()
        # context["form"] = forms.DynamicRequired4(
            # instance=animal)
        context["form"] = forms.DynamicRequired4()
        return render(request, template_name, context)

    def post(self, request):
        context = self.context
        template_name = "animal/dynamic_required_4.html"
        form = forms.DynamicRequired4(data=request.POST)
        if form.is_valid():
            # Notice the custom method!
            form.save_instance()
            url = reverse("animal:dynamic_required_4") + "?success=success"
            return redirect(url)
        else:
            context["form"] = form
            context["success"] = False
            template_name = "animal/dynamic_required_4.html"
            return render(request, template_name, context)
