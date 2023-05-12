from django.db import models
from django.utils.translation import gettext as _


class Isik(models.Model):
    """Õpilase mudel."""

    eesnimi = models.CharField(max_length=100)
    perenimi = models.CharField(max_length=100)


class Hinded(models.Model):
    """Hinde mudel."""

    kirjeldus = models.CharField(max_length=500)
    aine = models.CharField(max_length=50)


class IsikuHinne(models.Model):
    """Õpilase hinde mudel."""

    vaartus = models.CharField(max_length=1, choices=Hinded.choices)
    markmed = models.CharField(max_length=100)
    isik = models.ForeignKey(Isik, on_delete=models.CASCADE)
    hinne = models.ForeignKey(Hinded, on_delete=models.CASCADE)

    class Hinded(models.TextChoices):
        """Hinnete valikud."""

        VIIS = "5", _("5")
        NELI = "4", _("4")
        KOLM = "3", _("3")
        KAKS = "2", _("2")
        YKS = "1", _("1")
        X = "X", _("X")
