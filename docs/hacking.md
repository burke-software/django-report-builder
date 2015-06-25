#Hacking

You may of course run this as any django application.
However we've included some docker based tools and a demo project to make things easier.

##Running development environment with Docker [Compose]

This will get you a quick way to run report builder in a demo project - ideal for hacking on.

1. Install [Docker Compose](https://docs.docker.com/compose/) and Docker
2. Populate the database with `docker-compose run --rm web python manage.py migrate`.
3. Run `docker-compose up`
4. Go to `<docker host>:8000/report_builder`
4. You may want to edit `docker-compose.yml` to comment/uncomment the django-report-utils line. Report utils is a seperated library with common reporting functions. If you want to hack on report utils too just clone the repo in a sibling directory.

## Testing with docker-compose

Run `docker-compose run --rm web python manage.py test`.

## Styles

 Old code has the bad style I used at the time. New python code should follow pep8 standards.

 Pull requests should ideally include a unit test.

 User interface should follow Material Design guidelines - this is not strictly enforced.
