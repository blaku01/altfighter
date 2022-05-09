from django.db import models

# Create your models here.


class Stats(models.Model):
    class Meta:
        abstract = True
    strength = models.IntegerField(blank=True, null=True, default=0)
    agility = models.IntegerField(blank=True, null=True, default=0)
    vitality = models.IntegerField(blank=True, null=True, default=0)
    luck = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        text = f"{self.strength} {self.agility} {self.vitality} {self.luck}"
        return text

    def calculate_total_stats(self):
        return self.strength + self.agility + self.vitality + self.luck
