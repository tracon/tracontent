from setuptools import setup, find_packages


setup(
    name="tracontent",
    version="0.1",
    packages=find_packages(exclude=[
        'kompassi_oauth2',
        'site_specific',
        'tracontent',
    ]),
    install_requires=[
        'bleach>=2.0.0',
        'django-ckeditor>=5.3.0',
        'django-crispy-forms>=1.6.1',
        'django-ipware>=1.1',
        'django-reversion>=2.0.10',
        'Django>=1.9.13',
        'loremipsum>=1.0',
        'Pillow~=4.2.1',
        'python-dateutil>=2.6.1',
    ],
    author="Santtu Pajukanta",
    author_email="Santtu Pajukanta",
    description="TraContent CMS Enterprise Edition",
    license="MIT",
    keywords="cms",
)
