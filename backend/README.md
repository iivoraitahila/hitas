# Hitas backend for City of Helsinki

## Prerequisites

* [Python 3.10](https://www.python.org/)
* [Poetry >= 1.3.0](https://github.com/python-poetry/poetry#installation)
* [Docker](https://docs.docker.com/get-docker/)
  * alternatively PostgreSQL 13

## Get the Development Environment Up and Running

1. Clone this repository
2. Enter the backend directory `cd hitas/backend`
3. Start the app by running `make docker-build`
4. Access Django admin from [localhost:8080/admin](http://localhost:8080/admin). Default username `hitas`/`hitas`


### Running development environment without Docker

* Create a database for this project
* Install Python requirements: `poetry install`
* Enable debug `echo 'DEBUG=True' >> .env` [And setup env variables](#environment-variables)
* Run `python manage.py migrate`
* Run `python manage.py runserver`
* Access Django admin from [localhost:8000/admin](http://localhost:8080/admin). Default username `hitas`/`hitas`

## Testing

* Running the tests: `make tests`
* Running the tests without docker (local PostgreSQL required): `HITAS_TESTS_NO_DOCKER=1 make tests`

## Environment Variables

- Copy the template env file: `cp .env.template .env` and add values for the _placeholder_ variables in the `.env`
  file.

## Helpful commands

* Opening a shell in the container: `docker-compose run --rm hitas bash`
* Running code formatting and linting: `make format`
* Make a initial database dump: `make dump`

## API definitions

* It's possible to take a look into `openapi.yaml`
* After running `make docker-build` Swagger editor is running in [localhost:8090](localhost:8090)

## Git blame ignore refs

Project includes a `.git-blame-ignore-revs` file for ignoring certain commits from `git blame`.
This can be useful for ignoring e.g. formatting commits, so that it is more clear from `git blame`
where the actual code change came from. Configure your git to use it for this project with the
following command:

```shell
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

Git will now automatically look for the file when using `git blame`, no additional setup needed.

## Pre-commit hooks

* Pre-commit hooks are available for use in a local environment. They can be installed with
  `poetry run pre-commit install` and updated with `poetry run pre-commit autoupdate`.
* To skip running hooks during a commit, add a `--no-verify` flag to `git commit`.
* To run pre-commit on all files, use `poetry run pre-commit run --all-files`
