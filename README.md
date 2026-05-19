# Semantic Search Database

[![Test](https://github.com/acdh-oeaw/sem-search-db/actions/workflows/test.yml/badge.svg)](https://github.com/acdh-oeaw/sem-search-db/actions/workflows/test.yml)
[![Linting](https://github.com/acdh-oeaw/sem-search-db/actions/workflows/lint.yml/badge.svg)](https://github.com/acdh-oeaw/sem-search-db/actions/workflows/lint.yml)

A Django/Postgresql based database to process, store and expose textual data published through the project "Unified Corpora" via [corpus-search](https://corpus-search.acdh.oeaw.ac.at)

## install

* clone the repo
* change into the project's root directory e.g. `cd sem-search-db`
* run migrations `uv run manage.py migrate`
* start the dev sever `uv run manage.py runserver`
* go to [http://127.0.0.1:8000](http://127.0.0.1:8000/) and check if everything works

## data processing

To vectorize `TextSnippets` of a collection "TestCollection run

```shell
uv run manage.py create_embeddings --update --collection TestCollection
```

## Docker

At the ACDH-CH we use a centralized database-server. So instead of spawning a database for each service our services are talking to a database on this centralized db-server. This setup is reflected in the dockerized setting as well, meaning it expects an already existing database (either on your host, e.g. accessible via 'localhost' or some remote one)

### build the image

```shell
docker build -t semsearchdb:latest .
```

### run the image

```shell
docker run -it --network="host" --rm --env-file default.env --name semsearchdb semsearchdb:latest
```

-----

This project was bootstraped by [djangobase-cookiecutter](https://github.com/acdh-oeaw/djangobase-cookiecutter)
