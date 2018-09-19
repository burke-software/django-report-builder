# Hacking

You may of course run this as any django application.
However we've included some docker based tools and a demo project to make things easier.

## Running development environment with Docker Compose
This will get you a quick way to run report builder in a demo project - ideal for hacking on.

1. Clone the source code from [gitlab](https://gitlab.com/burke-software/django-report-builder). There's also a [github](https://github.com/burke-software/django-report-builder) repo that mirrors gitlab.
2. Install [Docker Compose](https://docs.docker.com/compose/) and Docker
3. Run `docker-compose build`
4. Populate the database with `docker-compose run --rm web python manage.py migrate`.
5. Run `docker-compose run --rm web ./manage.py createsuperuser` - use any credentials you like
6. Run `docker-compose up` - the django-admin for the sample back end should now be available at localhost:8000/admin.
7. log in at to `localhost:8000/admin` - necessary to use the report builder frontend!
8. Run `cd js; yarn install`
9. Run `yarn start` - once this finishes building the frontend should be available on localhost:4200

## Running the tests

Pull requests should include a unit test on any added behavior. If it fixes a
bug, it needs a failing test to show what it fixed. Documentation should also be
updated, if needed.

To test changes to the report-builder backend run `docker-compose run --rm web python manage.py test`.

Then to make sure your codes conforms to pep8:
```
docker-compose run --rm web flake8
```

To run tests with multiple Django versions run
`docker-compose run --rm web tox`
Please check django versions before submitting merge requests.

To run the angular tests simply cd into the js directory and run `yarn test`.

## Styles

Python code should follow pep8 standards. JS code uses [prettier](https://prettier.io/) for code formatting - we suggest installing [a plugin](https://prettier.io/docs/en/editors.html) to integrate it with your favorite editor.

## Opening issues

Please only open issues on Gitlab. Note this project is mostly in maintenance mode. It's fine to open wish list requests but the [Google Group](https://groups.google.com/forum/#!forum/django-report-builder) may be a better place.

If you want to make a major change and can put the time in to see it through, please open an issue to discuss first. If you are adding features that expand the scope of the project you should be prepared to help maintain them. There are many features I would LOVE to have but cannot commit the time to maintain myself.

## Making merge requests

1. Please make merge requests on https://gitlab.com/burke-software/django-report-builder. Do not use the github mirror.
2. Ensure tox passes first (See running tests section above).
3. Add a good description of what problem you are trying to solve and how you are trying to solve it.
4. Include unit tests whenever possible that would fail before your change and pass with your change.

# Frontend

The frontend is a angular app. We use ngrx (redux) for state management and angular-cli for scaffolding and tests.

# How to publish

1. `./build_js.sh` will compile the webpack bundle and move it to the django static folder
2. `python3 setup.py sdist bdist_wheel upload`
