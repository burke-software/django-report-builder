#Hacking

You may of course run this as any django application.
However we've included some docker based tools and a demo project to make things easier.

##Running development environment with Docker [Compose]

This will get you a quick way to run report builder in a demo project - ideal for hacking on.

1. Install [Docker Compose](https://docs.docker.com/compose/) and Docker
2. Populate the database with `docker-compose run --rm web python manage.py migrate`.
3. Run `docker-compose up`
4. Go to `<docker host>:8000/report_builder`
4. You may want to edit `docker-compose.yml` to comment/uncomment the django-report-utils line. Report utils is a separated library with common reporting functions. If you want to hack on report utils too just clone the repo in a sibling directory.

## Testing with docker-compose

Run `docker-compose run --rm web python manage.py test`.

Then to make sure your codes conforms to pep8:

```
docker-compose run --rm web flake8
```

## Styles

Python code should follow pep8 standards.

Pull requests should include a unit test on any added behavior. If it fixes a
bug, it needs a failing test to show what it fixed. Documentation should also be
updated, if needed.

User interface should follow Material Design guidelines - this is not strictly
enforced.

## Making pull requests

After you have a pull request that passes on Travis, and you have added
any needed test cases, please [squash your commits](http://gitready.com/advanced/2009/02/10/squashing-commits-with-rebase.html).
If it makes more sense to break it up into smaller commits, you can do that
as well. Just try to think what would be most helpful, when someone looks
back in the git history to see why this file was changed.

Thanks :)
