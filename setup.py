from setuptools import setup, find_packages

setup(
    name="kryten-reports",
    version="1.0.2",
    author="László Hegedűs",
    author_email="laszlo.hegedus@cherubits.hu",
    description=("Query and Report builder for Django ORM based on django-report-builder"),
    license="BSD",
    keywords="kryten django report material"    ,
    url="https://github.com/lordoftheflies/kryten-reports.git",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=[
        'openpyxl >= 2.2.1',
        'python-dateutil',
        'djangorestframework>=3.1.0',
        "six"
    ]
)
