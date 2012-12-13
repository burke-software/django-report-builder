from setuptools import setup, find_packages

setup(
    name = "django-report-builder",
    version = "1.4",
    author = "David Burke",
    author_email = "david@burkesoftware.com",
    description = ("Query and Report builder for Django ORM"),
    license = "BSD",
    keywords = "django report",
    url = "https://github.com/burke-software/django-report-builder",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=['openpyxl']
)
