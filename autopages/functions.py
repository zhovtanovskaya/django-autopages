# vim: set fileencoding=utf-8 fileformat=unix :

import os

from django.conf.urls import url
from django.views.generic.simple import direct_to_template


def get_templates(directory):
    """
    Get all templates in directory and subdirectories.
    """
    templates = []
    for path, subdirs, files in os.walk(directory):
        relpath = path.replace(directory, '')
        for template_name in files:
            template_path = os.path.join(relpath, template_name)
            if template_path.startswith(os.sep):
                template_path = template_path[1:]
            templates.append(template_path)
    return templates


def urlpattern_from_path(template_path, subdir=''):
    """
    Create list of URL-patterns from template paths.
    """
    if not template_path:
        return None
    if template_path.startswith(os.sep):
        template_path = template_path[1:]
    urlpath = os.path.splitext(template_path)[0]
    pattern = '^%s/$' % urlpath
    full_template_path = os.path.join(subdir, template_path)
    kwargs = {
        'template': full_template_path,
    }
    return url(pattern, direct_to_template, kwargs)
