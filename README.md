# Django Rest Framework Template

A simple setup with all the features I love.

## Extra Features

- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Django CORS Headers](https://github.com/adamchainz/django-cors-headers)
- [Django Admin Interface](https://github.com/fabiocaccamo/django-admin-interface)
- [Django Maintenance Mode](https://github.com/fabiocaccamo/django-maintenance-mode)
- [Django CKEditor](https://github.com/django-ckeditor/django-ckeditor)
- [Python Decuple](https://github.com/henriquebastos/python-decouple/)

## New Projects

In the [GitHub repo](https://github.com/ChrisCrossCrash/drf_project), click "Use this template" to make a new repo. The name should be suffixed with `_django` for consistancy.

The goal is to create a folder structure like this:
```
race
├───race_django
└───race_react
```
So, from the directory you want to make the entire project:
```
mkdir race
cd race
git clone <the url from the git repo>
```
Check the Python version and set up the virtual environment:
```
python -V
cd race_django
python -m venv venv
venv\scripts\activate
```
Check that the venv is activated, then install the requirments:
```
python -m pip install -r requirements.txt
```

Make a new `.env` file in the root directory. Paste this information inside:
```
# TODO: Modify these variables as needed
DEBUG=True
DJANGO_LOG_LEVEL=INFO
DJANGO_LOG_VERBOSITY=verbose
TIME_ZONE=Europe/Istanbul
MAINTENANCE_MODE=False

SECRET_KEY=
DOMAIN_NAME=example.com
#REACT_BUILD_PATH=
#EMAIL_HOST_USER=
#EMAIL_HOST_PASSWORD=
#EMAIL_HOST=email-smtp.us-east-2.amazonaws.com
```

Generate the new secret key in the command line with:
```
py -c "from django.core.management.utils import get_random_secret_key as x; print(x())"
```
Then, paste it into the `SECRET_KEY` variable in `.env` and save.

Finally, check the installation finish the setup:
```
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --email=chrislkumm@protonmail.com
python manage.py runserver
```

The project comes with a basic `Pizza` and `Toppings` model setup. Be sure to check the `TODO` items to see which example components should be removed.