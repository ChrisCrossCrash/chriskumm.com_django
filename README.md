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
- [Django Modern User](https://pypi.org/project/django-modern-user/)
- [Python Decuple](https://github.com/henriquebastos/python-decouple/)
- [Pillow](https://pillow.readthedocs.io/en/stable/)
- [Requests](https://2.python-requests.org/en/master/)
- [Black](https://black.readthedocs.io/en/stable/)
- [Pre-Commit](https://pre-commit.com/)

## Environment Variables

You'll have to copy the `.env.example` file to `.env` and fill in the values.

## Text Fixtures

Apps may contain a `fixtures/` directory, which contains its test fixtures.

Additionally, there is a `media/fixture/` directory which contains the media files for the fixtures. This directory is not ignored by Git.

To use the fixtures, simply run `python manage.py testserver [fixture [fixture ...]]`. This command loads the fixtures as test data which can be safely modified on the test server.

## Known Issues

### `dumpdata` in Windows

Using `python manage.py dumpdata -o somefile.json` in Windows (or at least PowerShell) will result in the following error:

```
(venv) PS C:\...\chriskumm.com_django> python .\manage.py dumpdata art | out-file -encoding UTF8 -noNewLine art_standard.json
CommandError: Unable to serialize database: 'charmap' codec can't encode character '\u02cc' in position 132: character maps to <undefined>
Exception ignored in: <generator object cursor_iter at 0x000001371B9280B0>
Traceback (most recent call last):
  File "C:\...\chriskumm.com_django\venv\lib\site-packages\django\db\models\sql\compiler.py", line 1649, in cursor_iter
    cursor.close()
sqlite3.ProgrammingError: Cannot operate on a closed database.
```

One way to get around this is by running the command from a virtual environment in WSL (Windows Subsystem for Linux).
