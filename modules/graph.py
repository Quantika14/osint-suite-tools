
import networkx as nx 
import matplotlib.pyplot as plt 

import modules.config as config

def get_GraphNodePersonalData(target):

    print("|----[INFO][GRAPH][>] starting to draw...")

    companies = config.companiesData_list
    emails = config.emailsData_list
    phones = config.phonesData_list
    DNIs = config.DNIData_list

    print (str(companies))

    g = nx.Graph()

    g.add_edge(target, "Companies")
    g.add_edge(target, "Phones")
    g.add_edge(target, "Emails")
    g.add_edge(target, "DNI")


    for company in companies:
        g.add_edge("Companies", company)
    
    for email in emails:
        g.add_edge("Emails", email)

    for phone in phones:
        g.add_edge("Phones", phone)
    
    for dni in DNIs:
        g.add_edge("DNI", dni)

    PNG = target.replace(" ", "-")
    nx.draw(g, with_labels = True) 
    plt.savefig(f"{PNG}.png") 
