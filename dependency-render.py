import csv
import graphviz

# columns of spreadsheet
COL_APPID   = 0
COL_APPNAME = 1
COL_GROUP   = 2
COL_VENDOR  = 3
COL_SLO     = 4
COL_DEPS    = 5

applications = {}
with open('dependencies.csv') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)
    for row in csvreader:
        deps = [] 
        if row[COL_DEPS]:
            deps = row[COL_DEPS].split(',')
        slo = None
        if (row[COL_SLO]):
            slo = float(row[COL_SLO])
        
        applications[row[COL_APPID]] = {
            'name': row[COL_APPNAME], 
            'group': row[COL_GROUP], 
            'vendor': row[COL_VENDOR], 
            'slo': slo, 
            'dependencies': deps
        }

dot = graphviz.Digraph(comment='Dependencies', 
    format='pdf', 
    graph_attr={'rankdir':'LR'},
    node_attr={'color': '#dddddd', 'style': 'filled', 'fontcolor':'#777777'},
    edge_attr={'color': 'darkgrey'})

for app_id, app in applications.items():
    for dep_id in app.get('dependencies'):
        if dep_id not in applications.keys():
            dot.node(dep_id, f'{dep_id}\n(undefined)', fillcolor='#eeeeee', color='#ff9999', style='dashed,filled')

for app_id, app in applications.items():
    app_name = app.get('name')
    app_slo = app.get('slo')
    slo_label = ''
    if app_slo:
        app_slo = float(app_slo)*100
        slo_label = f'\navailability: {app_slo}%'
        nodecolor   = 'white'
        textcolor   = 'black'
        bordercolor = 'black'
    else:
        nodecolor   = None
        textcolor   = None
        bordercolor = None

    if app.get('group'):
        group_name = app.get('group')
    else: 
        group_name = None
    
    vendor_label = app.get('vendor')
    if app.get('vendor'):
        vendor_label = f'\n({vendor_label})'

    dot.node(app_id, f'{app_name}{vendor_label}{slo_label}', cluster=group_name, group=group_name, color=bordercolor, fillcolor=nodecolor, fontcolor=textcolor)

    for dep_id in app.get('dependencies'):
        line_color='darkgrey'
        if dep_id in applications.keys():
            dep_slo = applications.get(dep_id).get('slo')
            if dep_slo:
                dep_slo = float(dep_slo)*100

            if (not app_slo) or (not dep_slo):
                line_color = None
            elif app_slo <= dep_slo:
                line_color='green'
            else:
                line_color='red'
        dot.edge(app_id, dep_id, dir='back', constraint='true', color=line_color)

dot.unflatten(stagger=3)
dot.render('dependencies.gv').replace('\\', '/')