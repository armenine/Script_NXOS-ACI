
########################################
# Create BD and/or its Unicast Routing #
########################################

# Excel File and Variables Jinja 
# Column 1 - Group
# Column 2 - client['l3out']['vlanid']
# Column 3 - client['tenant']
# Column 4 - client['l3out']['vrf']
# Column 5 - client['l3out']['name']
# Column 6 - client['tenant']['domain']
# Column 7 - client['node1001']['rtrId']
# Column 8 - client['node1002']['rtrId']
# Column 9 - client['node1501']['rtrId']
# Column 10 - client['node1502']['rtrId']
# Column 11 - client['node1001']['ip']
# Column 12 - client['node1002']['ip']
# Column 13 - client['node1501']['ip']
# Column 14 - client['node1502']['ip']
# Column 15 - client['node']['ipVip']
# Column 16 - client['node']['route-description']
# Column 17 - client['node']['nhAddr']
# Column 18 - client['l3out']['extEPG']['prefGrMemb']

import os
import openpyxl
from jinja2 import Environment, FileSystemLoader

# Load worksheet
wb = openpyxl.load_workbook('Input Files/NXOS_ACI_Info_baseline.xlsx')
sheet = wb["L3OUT"]


# Create a list to get datas
infoList = []

# Itere sobre as linhas na planilha
for row in list(sheet.iter_rows(values_only=True))[1:]:
    line = {
            'group' : row[0],
            'l3out': { 'vlanid': row[1], 'vrf': row[3], 'name': row[4], 'extEPG': { 'prefGrMemb': row[17] } },
            'tenant': { 'name' : row[2],'domain': row[5]},
            'node1001': { 'rtrId': row[6],'ip': row[10]},
            'node1002': { 'rtrId': row[7],'ip': row[11]},
            'node1501': { 'rtrId': row[8],'ip': row[12]},
            'node1502': { 'rtrId': row[9],'ip': row[13]},
            'node': { 'ipVip': row[14],'route-description': row[15],'nhAddr': row[16]}
     }

    infoList.append(line) 

for client in infoList:
    context = {'client': client} 
    # Load the template Jinja
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('templates/TEMPLATE_L3OUT_xml.jinja')

    # Fill teamplate with the datas
    output = template.render(context)
    
    # path file output
    path_file = f"Output/Grp_{client['group']}-{client['l3out']['name']}.xml"
    
    # Save the file output
    with open(path_file, 'w') as file:
        file.write(output)

