import os

import csv
import graphviz


class ApplicationNode:
    def __init__(self, name, group, vendor, important, slo, dependencies):
        self.name = name.strip()
        self.group = None if not group else group.strip()
        self.vendor = None if not vendor else vendor.strip()
        self.important = False if not important else True
        self.slo = None if not slo else float(slo)
        self.dependencies = set() if not dependencies else set([d.strip() for d in dependencies.split(',')])

class Config:
    # columns of CSV
    COL_APPID     = 0
    COL_APPNAME   = 1
    COL_GROUP     = 2
    COL_VENDOR    = 3
    COL_IMPORTANT = 4
    COL_SLO       = 5
    COL_DEPS      = 6

    skip_header = True

    show_legend = True

    def __init__(self, input_csv_path, output_type):
        self.input_csv_path = input_csv_path
        self.output_type = output_type
        self.output_filename = '.'.join(os.path.splitext(input_csv_path)[:-1 or 0]) + '.gv'


def row_to_application_node(config, row):
    return ApplicationNode(
                row[config.COL_APPNAME],
                row[config.COL_GROUP],
                row[config.COL_VENDOR],
                row[config.COL_IMPORTANT],
                row[config.COL_SLO],
                row[config.COL_DEPS]
            )


def ingest_applications_from_csv(config):
    '''
    parse CSV file; ignores first row.
    '''
    applications = {}
    with open(config.input_csv_path, "rt", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile)
        if config.skip_header:
            next(csvreader) # Skip header row
        for row in csvreader:
            applications[row[config.COL_APPID]] = row_to_application_node(config, row)

    return applications


def render_legend(legend):        
    legend.attr(cluster='true')
    legend.attr(label='Legend')
    legend.attr(color='black')
    legend.attr(bgcolor='white')
    legend.node('key', label='Application without SLO')
    legend.node('key2', label='Application with SLO', 
        color='black',
        fillcolor='white',
        fontcolor='black')
    legend.node('key3', label='Application with SLO', 
        fillcolor='#eeeeee',
        color='#ff9999', 
        fontcolor=None, 
        style='dashed,filled')
    with legend.subgraph(name='lines') as lines:
        lines.attr(cluster='false')
        lines.attr(shape='plaintext')
        lines.attr(rankdir='RL')
        lines.node('table1', label='''<<table border="0" cellpadding="2" cellspacing="0" cellborder="0">
                                      <tr><td align="right" port="i1">Dependency<br/>compatible SLO</td></tr>
                                      <tr><td align="right" port="i2">Dependency<br/>incompatible SLO</td></tr>
                                      <tr><td align="right" port="i3">Dependency<br/>unknown SLO</td></tr>
                                      </table>>''',
                   fillcolor='white',
                   color='white',
                   fontcolor='black')
        lines.node('table2', label='''<<table border="0" cellpadding="2" cellspacing="0" cellborder="0">
                                      <tr><td port="i1">&nbsp;<br/>&nbsp;</td></tr>
                                      <tr><td port="i2">&nbsp;<br/>&nbsp;</td></tr>
                                      <tr><td port="i3">&nbsp;<br/>&nbsp;</td></tr>
                                      </table>>''',
                    style='invis')
        lines.edge('table1:i1:w', 'table2:i1:e', color='green')
        lines.edge('table1:i2:w', 'table2:i2:e', color='red')
        lines.edge('table1:i3:w', 'table2:i3:e')



def dependency_set_to_graph(applications, config):
    '''
    Create graph
    '''

    dot = graphviz.Digraph(comment='Dependencies',
        graph_attr={'rankdir':'RL'},
        node_attr={'color': '#dddddd', 'style': 'filled', 'fontcolor':'#777777'},
        edge_attr={'color': 'darkgrey'})

    dot_endl = '<br />'

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
            slo_label   = ''
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

    # render legend
    if config.show_legend == True:    
        with dot.subgraph(name='legend') as legend:
            render_legend(legend)

    return dot


def render_output(config):
    dot = dependency_set_to_graph(ingest_applications_from_csv(config), config)
    dot.format=config.output_type
    dot.render(config.output_filename)

