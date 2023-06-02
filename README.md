# Hinded

## Nõuded
- Python (testitud 3.11-ga)
- Poetry
- SQLite driver
- Git
- Django

## Ülesseadmine
- Klooni GitHubi repositoorium: `git clone https://github.com/ks129/hinded.git`
- Installi vajalikud paketid terminalis: `poetry install`
- Lisa `.env` fail ning lisa sinna `DEBUG=1` (selleks, et admin korralikult töötaks) ning `SECRET_KEY=<suvaline väärtus>`.
- Loo andmebaas `poetry run task migrate`
- Loo esimene kasutaja `poetry run python manage.py createsuperuser`
- Käivita server `poetry run task start`
- Mine veebilehele http://localhost:8000 .
- Mine http://localhost:8000/admin ja lisa sealt kasutajaid kui vaja.
- Mine ülevalt paremast nurgast “VIEW SITE” ning saad hallata õpilaste hindeid.

Õpilasele saab lisada ligipääsukoodi, mille abiga saab "Vaata hindeid" nupuga (nähtav, kui pole sisse logitud) õpilane näha oma hindeid.
