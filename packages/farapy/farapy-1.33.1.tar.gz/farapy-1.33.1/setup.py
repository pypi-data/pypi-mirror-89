from setuptools import setup,find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_requires = [
    "Django>=2.2.7,<3",
    "django_jalali",
    "jdatetime",
    "django-ckeditor",
    "sorl-thumbnail",
    "kavenegar",
    "django-widget-tweaks",
    "Pillow>=4.0.0,<9.0.0",
    "simplejson",
    'copier',
]

setup(
    name='farapy',
    version='1.33.1',
    packages=['bin'],
    url='https://faral.tech',
    license='BSD',
    author='Faral Team',
    author_email='faral.ghaemi@gmail.com',
    description='FaraPy is a smart content management system (CMS) written in Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    install_requires=install_requires,
    entry_points="""
            [console_scripts]
            farapy=bin.farapy:main
    """,
)
