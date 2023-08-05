# djfim

Django extension of Fixture Import and Merge

## License

Apache License Version 2.0

## Usage

manage.py fim /path/to/fixture.json

## Config

It's as easy as 1-2-3.

1. Define a sub-class of `djfim.models.FURecord` in your application's `models.py`

```python
from djfim.models import FURecord

class YourAppFixture(FURecord):
    '''sub-class'''
    class Meta:
        abstract = False
```

2. Set up correct model name in your project's `settings.py`

```python
DJFIM = {
    'MODEL': {
        'app_name': 'demoapp',
        'app_label': 'YourAppFixture'
    }
}
```

3. Invoke the commands to update database schema

```bash
python manage.py makemigrations
python manage.py migrate
```

## Customize

Release number is automatically incremented each time the new fixture data is applied.

The release number increment policy is controlled via `RELEASE_INCREMENT_POLICY` field.
Currently only two options are available: `PLUS_ONE` and `PLUS_TEN`.

An example is shown below:

```python
# settings.py
DJFIM = {
    'RELEASE_INCREMENT_POLICY': 'PLUS_TEN',
    # other config items
    # ...
}
```

## TODO

- add unittest
- add support for user defined release number provider (or increment policy)
- drop support for Django 1.x and 2.x
