# Social Network

This is a homework solution for the OTUS "Highload Architect" course.

## Running

Make a copy of the `.env` file:

```shell
cp .env{.dist,}
```

To generate secrets keys and passwords use `openssl`:

```shell
openssl rand -hex 32
```

Start the stack:

```shell
make run-docker
```

Initialize the database:

```shell
make init-docker
```

See [Makefile](./Makefile) for more options.

## Heroku

```shell
heroku create
git push heroku main
heroku ps:scale web=1
heroku config:set \
    SECRET_KEY=xxx \
    FLASK_APP=supreme_umbrella.main:app
heroku addons:create jawsdb-maria:kitefin
```

Now see database URL:

```shell
heroku config
```

And configure environment accordingly:

```shell
heroku config:set \
    MYSQL_USER=xxx \
    MYSQL_PASSWORD=xxx \
    MYSQL_HOST=xxx.amazonaws.com \
    MYSQL_DATABASE=xxx
```

Now initialize the database:

```shell
heroku run flask init-db
```

## License

This is free and unencumbered software released into the public domain.

See [UNLICENSE](./UNLICENSE) file.
