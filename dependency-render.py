import copy
import csv
import json
import graphviz

input_data = {}
with open('dependencies.csv') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)
    for row in csvreader:
        deps = [] 
        if row[3]:
            deps = row[3].split(',')
        slo = None
        if (row[2]):
            slo = float(row[2])
        input_data[row[0]] = {"name": row[1], "slo": slo, "dependencies": deps}

#print(json.dumps(input_data, indent=4))

applications = copy.deepcopy(input_data)

dot = graphviz.Digraph(comment='Dependencies', format='png', 
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
        slo_label = f'\n{app_slo}%'
    
    if app.get('dependencies'):
        nodecolor   = 'white'
        textcolor   = 'black'
        bordercolor = 'black'
    else:
        nodecolor   = None
        textcolor   = None
        bordercolor = None

    dot.node(app_id, f'{app_name}{slo_label}', color=bordercolor, fillcolor=nodecolor, fontcolor=textcolor)

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
        dot.edge(app_id, dep_id, color=line_color)

dot.unflatten(stagger=3)
dot.render('dependencies.gv').replace('\\', '/')