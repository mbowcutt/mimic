from setuptools import setup

setup(
    name='Mimic',
    version='1.0',
    packages=['mimic'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-Migrate',
        'Flask-WTF',
        'Flask-Uploads',
        'markovify',
	'requests',
    ]
)
