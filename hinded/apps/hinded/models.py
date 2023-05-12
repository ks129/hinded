from django.db import models
# pylint: disable=undefined-variable
_ = lambda s: s

# Create your models here.

class Isik(models.Model):
    eesnimi = models.CharField(max_length = 100)
    perenimi = models.CharField(max_length = 100)

class Hinded(models.Model):
    kirjeldus = models.CharField(max_length = 500)
    aine = models.CharField(max_length = 50)

class IsikuHinne(models.Model):
     class Hinded(models.TextChoices):
        VIIS = "5", _("5")
        NELI = "4", _("4")
        KOLM = "3", _("3")
        KAKS = "2", _("2")
        YKS = "1", _("1")
        X = "X", _("X")
    vaartus = models.CharField(max_length = 1, choices= IsikuHinne.choices)
    markmed = models.CharField(max_length = 100)
    isik = models.ForeignKey(Isik, on_delete=models.CASCADE)
    hinne = models.ForeignKey(Hinded, on_delete=models.CASCADE)

