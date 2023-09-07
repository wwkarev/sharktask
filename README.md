### Install dependencies
1. Install dependencies `pip install -r requirements.txt`
2. Install dev dependencies `pip install -r requirements.dev.txt`

### Code style settings. Precommit hooks
1. Install hook `pre-commit install`
2. Run precommit checks `pre-commit run -a`


### Application start
`python manage.py runserver`

=====
# Shark task
=====

Shark task is a Django app implemented task manager api.

Quick start
-----------

1. Add "shark_task" to your INSTALLED_APPS setting like this::
```
INSTALLED_APPS = [
   ...,
   "django_shark_task",
]
```


2. Include the polls URLconf in your project urls.py like this::

   path("shark_task/", include("django_shark_task.urls")),

3. Run ``python manage.py migrate`` to apply the django_shark_task migrations.
