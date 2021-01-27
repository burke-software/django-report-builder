from setuptools import setup, find_packages

setup(
    name="django-report-builder",
    version="6.4.2",
    author="David Burke",
    author_email="david@burkesoftware.com",
    description=("Query and Report builder for Django ORM"),
    license="BSD",
    keywords="django report",
    url="https://gitlab.com/burke-software/django-report-builder",
    packages=find_packages(exclude=["report_builder_demo", "report_builder_demo.*"]),
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        "License :: OSI Approved :: BSD License",
    ],
    python_requires='>=3.3',
    install_requires=[
        'openpyxl >= 2.2.1',
        'python-dateutil',
        'djangorestframework>=3.8.0',
        "six"
    ]
)
