from setuptools import setup, find_packages

setup(
    name="django-report-builder",
    version="3.2.0",
    author="David Burke",
    author_email="david@burkesoftware.com",
    description=("Query and Report builder for Django ORM"),
    license="BSD",
    keywords="django report",
    url="https://github.com/burke-software/django-report-builder",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=[
        'django>=1.7',
        'openpyxl==2.2.1',
        'python-dateutil',
        'django-report-utils>=0.3.13',
        'djangorestframework>=3.0.4',
        "six"
    ]
)
