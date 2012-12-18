# vim: set fileencoding=utf-8 fileformat=unix :

from distutils.core import setup


setup(
    name='autopages',
    version='0.1',
    packages=[
        'autopages',
    ],
    install_requires=[
        'Django',
    ],
    description='Application for automatic URL recognition for templates',
    zip_safe=False,
)
