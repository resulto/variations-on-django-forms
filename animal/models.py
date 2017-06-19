from django.db import models


class AnimalType(models.Model):

    code = models.CharField(primary_key=True, max_length=10)
    label = models.CharField(max_length=250)

    def __str__(self):
        return self.label


class Activity(models.Model):
    animal_type = models.ForeignKey(
        AnimalType, related_name="activities")
    label = models.CharField(max_length=200)

    def __str__(self):
        return self.label


class Animal(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    type = models.ForeignKey(AnimalType, related_name="animals")
    favorite_activity = models.ForeignKey(
        Activity, related_name="favored_by_animals")
    activities = models.ManyToManyField(
        Activity, related_name="animals", blank=True)
    internal_notes = models.TextField(blank=True, default="")

    def __str__(self):
        return "{type}: {name} of age {age}. Favorite: {activity} "\
            "({count} activities)".format(
                type=self.type.label, name=self.name, age=self.age,
                activity=self.favorite_activity.label,
                count=self.activities.count())
