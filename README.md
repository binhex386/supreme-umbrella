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

## License

This is free and unencumbered software released into the public domain.

See [UNLICENSE](./UNLICENSE) file.
