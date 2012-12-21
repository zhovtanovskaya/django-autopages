django-autopages
================

This application scans specified directories with Django-templates and 
adds URL for every template it finds using Django's view `direct_to_templates`.

Installation
------------

1. Install package from repository:

        pip install -e git+git://github.com/zhovtanovskaya/django-autopages.git#egg=autopages

2. Add `'autopages'` to your `settings.INSTALLED_APPS`.
3. Add following lines to your `urls.py`:

        from autopages.urls import autopages
        
        urlpatterns += autopages('autopages')
    
4. Now you can add templates to `templates/autopages/` and __after restart of server__ you'll 
be able to see them. E.g. for template `templates/autopages/about.html` corresponding URL is 
`/about/`, and for `templates/autopages/more/faq.html` URL is `/more/faq/`.
