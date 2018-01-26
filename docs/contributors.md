# Hacking

You may of course run this as any django application.
However we've included some docker based tools and a demo project to make things easier.

## Running development environment with Docker Compose
This will get you a quick way to run report builder in a demo project - ideal for hacking on.

1. Clone the source code from [gitlab](https://gitlab.com/burke-software/django-report-builder). There's also a [github](https://github.com/burke-software/django-report-builder) repo that mirrors gitlab.
2. Install [Docker Compose](https://docs.docker.com/compose/) and Docker
3. Run `docker-compose build`
4. Populate the database with `docker-compose run --rm web python manage.py migrate`.
5. Run `docker-compose run web --rm ./manage.py createsuperuser` - use any credentials you like
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

## Making pull requests

After you have a pull request that passes on Travis, and you have added
any needed test cases, please [squash your commits](http://gitready.com/advanced/2009/02/10/squashing-commits-with-rebase.html).
If it makes more sense to break it up into smaller commits, you can do that
as well. Just try to think what would be most helpful, when someone looks
back in the git history to see why this file was changed.

Thanks :)

# Frontend

The frontend is a angular app. We use ngrx (redux) for state management and angular-cli for scaffolding and tests.

# How to publish

1. `./build_js.sh` will compile the webpack bundle and move it to the django static folder
2. `python3 setup.py sdist bdist_wheel upload`