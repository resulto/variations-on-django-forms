import json

from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse

from animal import forms
from animal.models import Animal, Activity, AnimalType


class AnimalView(View):

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
            template_name = "animal/home.html"
            return render(request, template_name, context)


class DynamicRequired1(AnimalView):

    def get(self, request):
        context = self.context
        template_name = "animal/dynamic_required_1.html"
        context["success"] = request.GET.get("success") == "success"
        context["form"] = forms.DynamicRequired1()
        print(list(context["form"].fields["type"].choices))
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
            template_name = "animal/dynamic_required_1.html"
            return render(request, template_name, context)


class DynamicRequired2(AnimalView):

    def get(self, request):
        context = self.context
        template_name = "animal/dynamic_required_2.html"
        context["success"] = request.GET.get("success") == "success"
        context["form"] = forms.DynamicRequired2()
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
            template_name = "animal/dynamic_required_2.html"
            return render(request, template_name, context)
