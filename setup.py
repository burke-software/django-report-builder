from setuptools import setup, find_packages

setup(
    name = "django-report-builder",
    version = "2.0.2",
    author = "David Burke",
    author_email = "david@burkesoftware.com",
    description = ("Query and Report builder for Django ORM"),
    license = "BSD",
    keywords = "django report",
    url = "https://github.com/burke-software/django-report-builder",
    packages=find_packages(),
    include_package_data=True,
    test_suite='setuptest.setuptest.SetupTestSuite',
    tests_require=(
        'django-setuptest',
        'argparse',
    ),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=[
        'django>=1.4',
        'openpyxl',
        'python-dateutil',
        'django-report-utils>=0.2.3',
    ]
)
