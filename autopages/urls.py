# vim: set fileencoding=utf-8 fileformat=unix :

import logging

from django.conf.urls import patterns
from django.template import loader

from autopages.functions import (
    get_templates,
    urlpattern_from_path,
)


logger = logging.getLogger(__name__)


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
        logger.debug('Getting templates from loader "%s".' % l)
        if hasattr(l, 'get_template_sources'):
            directories = l.get_template_sources(dirname)
            logger.debug('"%s" directories: %s.' % (l, directories))
            for directory in directories:
                dirtemplates = get_templates(directory)
                msg = 'Directory "%s" templates: %s.' % (
                    directory, dirtemplates)
                logger.debug(msg)
                templates.extend(dirtemplates)
        else:
            msg = 'Loader "%s" has no attribute `template_source_loaders`.' % l
            logger.debug(msg)

    urls = []
    for template in templates:
        pattern = urlpattern_from_path(template, dirname)
        logger.debug(
            'Adding URL-pattern "%s" for template "%s".' % (pattern, template))
        urls.append(pattern)
    return patterns('', *urls)
