# vim: set fileencoding=utf-8 fileformat=unix :

from django.conf.urls import patterns
from django.template import loader

from autopages.functions import (
    get_templates,
    urlpattern_from_path,
)


def autopages(dirname='autopages'):
    """
    Create URL-patterns for templates in template directory.

    If we have:
    autopages/
    |- about.html
    `- company/
       ` products.html
    The return value is:
    patterns('',
        url('^about/$', direct_to_template,
            {'template': 'autopages/about.html'}),
        url('^company/products/$', direct_to_template,
            {'template': 'autopages/company/products.html'}),
    )
    """
    templates = []
    try:
        loader.find_template('')
    except loader.TemplateDoesNotExist:
        pass
    for l in loader.template_source_loaders:
        if hasattr(l, 'get_template_sources'):
            for directory in l.get_template_sources(dirname):
                dirtemplates = get_templates(directory)
                templates.extend(dirtemplates)
    urls = []
    for template in templates:
        pattern = urlpattern_from_path(template, dirname)
        urls.append(pattern)
    return patterns('', *urls)
