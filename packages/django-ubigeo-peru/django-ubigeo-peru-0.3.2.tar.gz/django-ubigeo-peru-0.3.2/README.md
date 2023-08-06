# Django-Ubigeo-Peru

django-ubigeo-peru, is an app that will allow you to easily implement the ubiquites of INEI (Perú) in your django app.


## Config

In your settings.py

```python
    INSTALLED_APPS = (
        ....
        'ubigeos',
    )
```
Run

```bash
python manage.py migrate
python manage.py loaddata ubigeos.json
```

In your urls.py

For Django <= 1.11.x

```python
    urlpatterns = patterns('',
        ....
        (r'^ubigeos/', include('ubigeos.urls')),
    )
```
For Django 2.x

```python
    urlpatterns = patterns('',
        ....
        path('ubigeos/', include('ubigeos.urls')),
    )
```


## License
BSD
