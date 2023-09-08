# dependency-render

This renders a graph of dependencies. It takes as input a CSV called `dependencies.csv`, and uses Graphviz to generate a dependency map as a PDF.

## usage

You need to install the [`graphviz`](https://pypi.org/project/graphviz/) and [`argparse`](https://pypi.org/project/argparse/) packages in python. To do this, do:

```bash
pip install graphviz argparse
```

usage: `dependency-render.py [--output-type {pdf,png,svg}] input_csv`

Dependency graph generator

positional arguments:
- `input_csv`: The CSV to parse

optional arguments:
- `--output-type`: Output file type for the graph to render. Valid types are `pdf`, `png`, and `svg`. Default is `pdf`.

Example:
```bash
python3 dependency-render.py dependencies.csv --output-type=svg
```

## CSV format

It should be formatted with the following columns:

1. Application ID
2. Application Name
3. group
4. vendor
5. Availability SLO
6. Dependencies


### Example

| Application ID | Application Name | group | vendor | Availability SLO | Dependencies              |
| -------------- | ---------------- | ----- | ------ | ---------------- | ------------------------- |
| foo            | Foo Application  |       |        | 0.99             | bar,baz,google-maps       |
| bar            | Bar API          | api   |        | 0.999            | mongo,okta                |
| baz            | Baz API          | api   |        | 0.999            | mongo,okta                |
| quux           | Quux API         | api   |        | 0.99             |                           |
| google-maps    | Google Maps API  |       | Google |                  |                           |
| okta           | Okta Core API    |       | Okta   |                  |                           |

See [`example.csv`](./example.csv)

The above will render to:

![Example graph](./example.svg)
