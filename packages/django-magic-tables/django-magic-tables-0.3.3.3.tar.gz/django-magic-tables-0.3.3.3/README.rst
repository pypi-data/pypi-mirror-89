=====
Magic Tables
=====

Magic Tables is a Django app to turn QuerySets into any kind of table.

Detailed documentation is in the "docs" directory.

Quick start
-----------

- Install package

    ::
        
        $ pip install django-magic-tables


- Add "magic_tables" to your INSTALLED_APPS setting like this:

    ::

        INSTALLED_APPS = [
            ...
            'magic_tables',
        ]


- Load "magic_tables_tags" at the top of the page where you want to use them like this:

    ::

        {% load magic_tables_tags %}
        [...]


- Create a magic table:

    ::

        [...]

        {% table object_list "optional classes separated by spaces" %}
    
        [...]


Use it with Datatable
-----------

- Include CSS 

    ::

        <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.21/css/dataTables.bootstrap4.min.css">
        <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/responsive/2.2.4/css/responsive.bootstrap4.min.css">


- Include JS
    
    ::

        <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.21/js/jquery.dataTables.js"></script>
        <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.21/js/dataTables.bootstrap4.min.js"></script>
        <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/responsive/2.2.4/js/dataTables.responsive.min.js"></script>
        <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/responsive/2.2.4/js/responsive.bootstrap4.min.js"></script>
        <script>
            $(document).ready( function () {
                $('.data-table').DataTable( {
                    'language': {
                        'lengthMenu': '_MENU_ Results for page',
                        'zeroRecords': 'No results',
                        'info': 'Page _PAGE_ of _PAGES_',
                        'infoEmpty': 'No results',
                        'infoFiltered': '(Filtered on _MAX_ total results)',
                        'search': 'Search: ',
                        'paginate': {
                            'first': 'First',
                            'last': 'Last',
                            'next': 'Next',
                            'previous': 'Previous'
                        }
                    },
                    'initComplete': () => { $('.data-table').fadeIn(); $('.graph').fadeIn(); }
                } );
            } );
        </script>
    
- Pass "data-table" as second parameter to the table tag like this:

    ::

        {% table object_list "data-table" %}