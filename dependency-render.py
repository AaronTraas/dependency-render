import copy
import json

input_data = {
    "sets-api-v2": { "name": "Sets API V2", "slo": 0.99, "dependencies": ["experiments-api", "materials", "line-advancements" ] },
    "sets-api-v3": { "name": "Sets API V3", "slo": 0.99, "dependencies": ["experiments-api", "materials", "line-advancements" ] },
    "harvest-analytics": { "name": "Harvest Analytics Orchestrator", "slo": 0.99, "dependencies": ["sets-api-v2", "qanda-api", "job-inputs", "l360-geoserver", "capacity-request", "experiments-api", "capacity-request", "plans-api"] }
}

applications = copy.deepcopy(input_data)

uml_out = '@startuml\n'
for app_id, app in applications.items():
    app_name = app.get('name')
    uml_out += (f'\n[{app_name}] as [{app_id}]\n')
    for dep_id in app.get('dependencies'):
        uml_out += (f'[{dep_id}] -> [{app_id}]\n')
uml_out += ('\n@enduml\n')

print(uml_out)