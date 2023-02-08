# Toudou

The best todo application!


## Installing

```bash
$ pip install -U toudou
```

## Usage

```bash
$ toudou
Usage: toudou [OPTIONS] COMMAND [ARGS]...

Options:
    --help  Show this message and exit.

Commands:
    create
    get
    get-all
    import-csv
    init-db
    update
```


## Contributing

Start coding using an editable project with:

```bash
$ python3 -m venv venv
$ source ./venv/bin/activate
(venv) $ pip install -e .
(venv) $ toudou
```

Or with PDM:

```bash
$ pdm install
$ pdm run toudou
```