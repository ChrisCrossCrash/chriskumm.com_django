# ChrisKumm.com Django Back End

A simple Django back end for my portfolio site.

## Features

- InstaArt API: REST API for [InstaArt](https://api.chriskumm.com/art)
- Admin page: A dashboard for managing everything in the database

## Third-Party Libraries

- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Django CORS Headers](https://github.com/adamchainz/django-cors-headers)
- [Django Admin Interface](https://github.com/fabiocaccamo/django-admin-interface)
- [Django CKEditor](https://github.com/django-ckeditor/django-ckeditor)
- [Python Decuple](https://github.com/henriquebastos/python-decouple/)

## Environment Variables
You'll need to create a file named `.env` in the root directory of this project and populate it with the following environment variables:
```
# Is this a development or production environment? (boolean)
DEBUG=

# What time zone is the server running in? (Example: Europe/Istanbul)
TIME_ZONE=

# The Django secret key (you can just make something up if this is not for production)
SECRET_KEY=

# Abuse API key (for checking if an IP address is abusive)
# https://www.abuseipdb.com/account/api
ABUSEIPDB_API_KEY=

# Email Settings
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_HOST=

```
