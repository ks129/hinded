from django.db import models
from django.utils.translation import gettext as _


class Isik(models.Model):
    """Õpilase mudel."""

    eesnimi = models.CharField(max_length=100)
    perenimi = models.CharField(max_length=100)

    def __str__(self) -> str:
        """Näita administratsioonis õpilase nime."""
        return f"{self.eesnimi} {self.perenimi}"


class Hinded(models.Model):
    """Hinde mudel."""

    nimi = models.CharField(max_length=100, default="Kontrolltöö")
    kirjeldus = models.CharField(max_length=500, blank=True, default="")
    aine = models.CharField(max_length=50)

    def __str__(self) -> str:
        """Näita administratsioonis hinde nime."""
        return self.nimi


class IsikuHinne(models.Model):
    """
    Õpilase hinde mudel.

    Selle mudeli puhul pole __str__ funktsiooni lisatud,
    kuna see kutsuks välja rohkem SQL päringuid ehk
    muudaks lehe aeglasemaks.
    """

    class HinneteValik(models.TextChoices):
        """Hinnete valikud."""

        VIIS = "5", _("5")
        NELI = "4", _("4")
        KOLM = "3", _("3")
        KAKS = "2", _("2")
        YKS = "1", _("1")
        X = "X", _("X")

    vaartus = models.CharField(max_length=1, choices=HinneteValik.choices)
    markmed = models.CharField(max_length=100, blank=True, default="")
    isik = models.ForeignKey(Isik, on_delete=models.CASCADE)
    hinne = models.ForeignKey(Hinded, on_delete=models.CASCADE)

    class Meta:
        """Keela ühele õpilasele ühte hinnet mitu korda lisada."""

        constraints = [
            models.UniqueConstraint(fields=["isik", "hinne"], name="unikaalne_nimi_hinne")
        ]
