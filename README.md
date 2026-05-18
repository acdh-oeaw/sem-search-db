# Semantic Search Database

A Django/Postgresql based database to process, store and expose textual data published through the project "Unified Corpora" via [corpus-search](https://corpus-search.acdh.oeaw.ac.at)

## install

* clone the repo
* change into the project's root directory e.g. `cd sem-search-db`
* run migrations `uv run manage.py migrate`
* start the dev sever `uv run manage.py runserver`
* go to [http://127.0.0.1:8000](http://127.0.0.1:8000/) and check if everything works

## Docker

At the ACDH-CH we use a centralized database-server. So instead of spawning a database for each service our services are talking to a database on this centralized db-server. This setup is reflected in the dockerized setting as well, meaning it expects an already existing database (either on your host, e.g. accessible via 'localhost' or some remote one)

### building the image

* `docker build -t semsearchdb:latest .`
* `docker build -t semsearchdb:latest --no-cache .`

### running the image

To run the image you should provide an `.env` file to pass in needed environment variables; see example below:

* `docker run -it -p 8020:8020 --rm --env-file default.env --name semsearchdb semsearchdb:latest`

-----

This project was bootstraped by [djangobase-cookiecutter](https://github.com/acdh-oeaw/djangobase-cookiecutter)