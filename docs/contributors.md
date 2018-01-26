To contribute to django-report-builder, please check out our source code on [gitlab](https://gitlab.com/burke-software/django-report-builder) or [github](https://github.com/burke-software/django-report-builder).

To install:
1. `docker-compose build`
2. `docker-compose run web --rm ./manage.py migrate`
3. `docker-compose run web --rm ./manage.py createsuperuser` - use any credentials you like
4. `docker-compose up` - the django-admin for the example back end should now be available at localhost:8000/admin.
5. log in at to `localhost:8000/admin` - necessary to use the frontend!
6. `cd js; yarn install`
7. `yarn start` - once this finishes building the frontend should be available on localhost:4200

Things to keep in mind while contributing:
* Adding a new feature? Consider adding a test as well!
* If your branch doesn't pass CI, it won't get merged! Just because the tests are broken doesn't mean your code is bad - but if you're submitting a change, change any broken tests so they pass as well!