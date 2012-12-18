# vim: set fileencoding=utf-8 fileformat=unix :

import os
import re

from django.conf import settings
from django.conf.urls import patterns, url, include
from django.test import TestCase
from django.views.generic.simple import direct_to_template
from shutil import rmtree

from autopages.functions import (
    get_templates,
    urlpattern_from_path,
)
from autopages.urls import autopages


class UrlpatternFromPathTest(TestCase):

    def test_page_name(self):
        path = 'about.html'
        urlpattern = urlpattern_from_path(path)
        regex = re.compile(r'^about/$', re.UNICODE)
        self.assertEquals(regex, urlpattern.regex)

    def test_page_path(self):
        path = 'dir/about.html'
        urlpattern = urlpattern_from_path(path)
        regex = re.compile(r'^dir/about/$', re.UNICODE)
        self.assertEquals(regex, urlpattern.regex)

    def test_default_args(self):
        path = 'dir/about.html'
        dirname = 'a'
        urlpattern = urlpattern_from_path(path, dirname)
        self.assertEquals(
            {'template': os.path.join(dirname, path)}, urlpattern.default_args)


class TemplateTestCase(TestCase):

    def _create_templates(self, templates, base_dir):
        for template in templates:
            template_path = os.path.join(base_dir, template)
            dirs = os.path.split(template_path)[0]
            try:
                os.makedirs(dirs)
            except OSError:
                pass
            with open(template_path, 'w'):
                pass


class GetTemplatesTest(TemplateTestCase):

    def setUp(self):
        self.templates = sorted([
            'a/b.html',
            'c.html',
            'd/e/f.html',
        ])
        self.base_dir = os.path.join(settings.BASE_PATH, 'test_autopages')
        self._create_templates(self.templates, self.base_dir)

    def tearDown(self):
        rmtree(self.base_dir)

    def test_files_list(self):
        templates = get_templates(self.base_dir)
        self.assertEquals(self.templates, sorted(templates))


class AutopagesTest(TemplateTestCase):

    def setUp(self):
        self.templates = [
            'a/b.html',
            'c.html',
            'd/e/f.html',
        ]
        self.patterns = patterns('',
            url('^c/$', direct_to_template, {'template': '_test_autopages/c.html'}),
            url('^a/b/$', direct_to_template, {'template': '_test_autopages/a/b.html'}),
            url('^d/e/f/$', direct_to_template, {'template': '_test_autopages/d/e/f.html'}),
        )
        self.dirname = '_test_autopages'
        self.base_dir = os.path.join(settings.TEMPLATE_DIRS[0], self.dirname)
        self._create_templates(self.templates, self.base_dir)

    def tearDown(self):
        rmtree(self.base_dir)

    def test_patterns(self):
        patterns = autopages(self.dirname)
        self.assertNotEqual([], patterns)
        for index in range(len(self.patterns)):
            exp = self.patterns[index]
            got = patterns[index]
            self.assertEquals(exp.regex.pattern, got.regex.pattern)
            self.assertEquals(exp.default_args, got.default_args)
