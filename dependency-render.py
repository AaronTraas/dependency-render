#!/usr/bin/env python3

import os

import argparse
import csv
import graphviz


class ApplicationNode:
    def __init__(self, name, group, vendor, slo, dependencies):
        self.name = name
        self.group = None if not group else group
        self.vendor = vendor
        self.slo = None if not slo else float(slo)
        self.dependencies = set() if not dependencies else set(dependencies.split(','))


class Config:
    # columns of CSV
    COL_APPID   = 0
    COL_APPNAME = 1
    COL_GROUP   = 2
    COL_VENDOR  = 3
    COL_SLO     = 4
    COL_DEPS    = 5

    def __init__(self, input_csv_path, output_type):
        self.input_csv_path = input_csv_path
        self.output_type = output_type
        self.output_filename = '.'.join(os.path.splitext(input_csv_path)[:-1 or 0]) + '.gv'


def cli_args_to_config():
    '''
    parse command-line args
    '''
    parser = argparse.ArgumentParser(description='Dependency graph generator')
    parser.add_argument('input_csv',
        help='The CSV to parse')
    parser.add_argument('--output-type', choices=['pdf','png','svg'], default='pdf',
        help='Output file type for the graph to render.')
    args = parser.parse_args()

    return Config(args.input_csv, args.output_type)


def ingest_applications_from_csv(config):
    '''
    parse CSV file; ignores first row.
    '''
    applications = {}
    with open(config.input_csv_path, "rt", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader) # Skip header row
        for row in csvreader:
            applications[row[config.COL_APPID]] = ApplicationNode(
                row[config.COL_APPNAME],
                row[config.COL_GROUP],
                row[config.COL_VENDOR],
                row[config.COL_SLO],
                row[config.COL_DEPS]
            )

    return applications


def dependency_set_to_graph(applications):
    '''
    Create graph
    '''

    dot = graphviz.Digraph(comment='Dependencies',
        graph_attr={'rankdir':'RL'},
        node_attr={'color': '#dddddd', 'style': 'filled', 'fontcolor':'#777777'},
        edge_attr={'color': 'darkgrey'})

    dot_endl = '<BR />'

    # create nodes that only exist as dependencies, but aren't defined as rows in the CSV.
    all_deps = set.union(*[ app.dependencies for app in applications.values() ])
    known_apps = set(applications.keys())
    # undefined_deps = all_deps - known_apps
    for dep_id in all_deps.difference(known_apps):
        dot.node(dep_id, f'<{dep_id}{dot_endl}(undefined)>', fillcolor='#eeeeee',
                 color='#ff9999', fontcolor=None, style='dashed,filled')

    # create node and connections for each defined applications
    for app_id, app in applications.items():
        if app.slo:
            slo_label   = f'{dot_endl}availability: {app.slo*100}%'
            nodecolor   = 'white'
            textcolor   = 'black'
            bordercolor = 'black'
        else:
            slo_label   = '' #f'{dot_endl}availability: N/A'
            nodecolor   = None
            textcolor   = None
            bordercolor = None

        vendor_label = '' if not app.vendor else f'{dot_endl}({app.vendor})'

        group_name = app.group

        dot.node(app_id, f'<{app.name}{vendor_label}{slo_label}>',
                 group=group_name, color=bordercolor,
                 fillcolor=nodecolor, fontcolor=textcolor)

        # create connections to dependencies
        for dep_id in app.dependencies:
            line_color=None
            if dep_id in known_apps:
                dep_slo = applications.get(dep_id).slo

                if (app.slo is not None) and (dep_slo is not None):
                    line_color='green' if app.slo <= dep_slo else 'red'

            dot.edge(dep_id, app_id, color=line_color)

    return dot


def render_output(config, dot):
    dot.format=config.output_type
    dot.render(config.output_filename)


if __name__ == '__main__':
    g_config = cli_args_to_config()

    g_applications = ingest_applications_from_csv(g_config)

    g_dot = dependency_set_to_graph(g_applications)

    render_output(g_config, g_dot)
