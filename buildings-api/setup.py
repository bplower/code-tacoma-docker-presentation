from setuptools import setup

setup(
    name = 'buildings_api',
    version = '0.1.0',
    description = 'An API about tall buildings',
    author = 'Brahm Lower',
    author_email = 'bplower@gmail.com',

    py_modules = ["buildings_api"],
    install_requires = [
        'Flask',
        'PyYAML',
        'psycopg2-binary'
    ],
    entry_points = {
        'console_scripts': [
            'buildings-api=buildings_api:main'
        ]
    },
    project_urls = {
        'Source': 'https://github.com/bplower/docker-presentation/buildings-api'
    }
)