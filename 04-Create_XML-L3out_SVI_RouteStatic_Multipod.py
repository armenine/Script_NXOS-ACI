
########################################
# Create BD and/or its Unicast Routing #
########################################

# Excel File and Variables Jinja 


import os
import openpyxl
from jinja2 import Environment, FileSystemLoader
import ast

# Load worksheet
wb = openpyxl.load_workbook('Input Files/NXOS_ACI_Info_baseline.xlsx')
sheet = wb["L3OUT"]

# Create a list to get datas
infoList = []

# Função para verificar se a linha já está na lista
def is_duplicate(line, infoList):
    for existing_line in infoList:
        if existing_line == line:
            return True
    return False

# Itere sobre as linhas na planilha
for row in list(sheet.iter_rows(values_only=True))[1:]:
 # Verificar se a linha tem pelo menos uma célula não vazia
    if any(row):
        line = {
            'group': row[0],
            'l3out': {
                'vlanid': row[1],
                'vrf': row[3],
                'name': row[4]
            },
            'tenant': {'name': row[2], 'l3domain': row[5]},
            'nodeProf': {
                'name-nodeProf-pod1': row[6],
                'name-nodeProf-pod2': row[7],
                'node-105-rtrId': row[9],
                'node-106-rtrId': row[10],
                'node-205-rtrId': row[11],
                'node-206-rtrId': row[12]
            },
            'path': {
                'path-node-105-106': row[13],
                'path-node-205-206': row[14]
            },
            'intProf': {
                'name-IntProf': row[8],
                'node-105-IP': row[15],
                'node-106-IP': row[16],
                'node-205-IP': row[17],
                'node-206-IP': row[18],
                'node-IP-VIP': row[19]
            },
            'extepg-name': row[20],
            'contracts': True if row[23] == 'yes' else False,
            'routes': ast.literal_eval(row[21]) if row[21] else [],
            'extepg': ast.literal_eval(row[22]) if row[22] else []
        }
    if not is_duplicate(line, infoList):
        infoList.append(line) 



for client in infoList:
    context = {'client': client} 

    # Load the template Jinja
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('templates/template-l3out_xml.jinja')

    # Fill teamplate with the datas
    output = template.render(context)
    
    # path file output
    path_file = f"Output/Grp_{client['group']}-{client['l3out']['name']}.xml"
    
    # Save the file output
    with open(path_file, 'w') as file:
        file.write(output)

    # Rollback 
    context['Rollback'] = True

    
    # Fill teamplate with the datas
    output = template.render(context)

    # path file output
    path_file = f"Output/Grp_{client['group']}-{client['l3out']['name']}_Rollback.xml"

    # Save the file output
    with open(path_file, 'w') as file:
        file.write(output)
