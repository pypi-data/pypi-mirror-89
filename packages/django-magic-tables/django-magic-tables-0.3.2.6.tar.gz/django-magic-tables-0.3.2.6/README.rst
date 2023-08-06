=====
Magic Tables
=====

Magic Tables is a Django app to turn QuerySets into any kind of table.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Install package

   $ pip install django-magic-tables'


- Add "magic_tables" to your INSTALLED_APPS setting like this:

    ::

        INSTALLED_APPS = [
            ...
            'magic_tables',
        ]


3. Load "magic_tables_tags" at the top of the page where you want to use them like this:

    {% load magic_tables_tags %}
    [...]


4. Create a magic table:

    [...]

    {% table object_list "optional classes separated by spaces" %}
    
    [...]