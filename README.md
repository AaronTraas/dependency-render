# dependency-render

This renders a graph of dependencies. It takes as input a CSV called `dependencies.csv`, and uses Graphviz to generate a dependency map as a PDF.

## usage

You need to install the [`graphviz` package](https://pypi.org/project/graphviz/) in python. To do this, do:

```bash
$ pip install graphviz
```

## CSV format

It should be formatted with the following columns:

Application ID  Application Name    group   vendor  Availability SLO    Dependencies

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