from html_reports.reports import Report
from datetime import datetime
from datetime import timedelta

import modules.data as data

rep = Report()



def generate_report(target):
    print ("Generando el informe")
    now = datetime.now()

    rep.add_title(f"INFORME {now}")
    rep.add_title("BUSCADOR DE PERSONAS", level=2)
    rep.add_markdown("![alt text](images/DG-minimal-version.png 'Logo DG')")
    rep.add_markdown("=====================================================")
    rep.add_markdown(f"- Target: {target}")
    rep.add_markdown("=====================================================")

    rep.add_title("[Análisis de frecuencia del nombre y apellidos en España]", level = 3)
    rep.add_markdown("Información sobre la fuente: www.ine.es")
    rep.add_markdown(f"- Nº de frecuencia del nombre masculino: {data.INE_name_man}")
    rep.add_markdown(f"- Nº de frecuencia del nombre femenino: {data.INE_name_woman}")
    rep.add_markdown(f"- Nº de frecuencia del primer apellido: {data.INE_surname}")
    rep.add_markdown(f"- Nº de frecuencia del segundo apellido: {data.INE_second_surname}")
 

    rep.add_title("[Información personal.]", level = 3)
    rep.add_markdown("Información sobre la fuente: www.wikipedia.com")
    rep.add_markdown(f"- URL: {data.Wiki_url}")
    rep.add_markdown(f"- Fecha y lugar de nacimiento: {data.Wiki_birth}")
    rep.add_markdown(f"- Fecha de fallecimiento: {data.Wiki_death}")
    rep.add_markdown(f"- Ocupación profesional : {data.Wiki_employment}")
    rep.add_markdown(f"- Nº de hijos: {data.Wiki_sons}")
    rep.add_markdown(f"- Religión: {data.Wiki_religion}")
    rep.add_markdown(f"- Partido Políticos: {data.Wiki_politicalParty}")
    rep.add_markdown(f"- Horóscopo: {data.Wiki_horoscopo}")


    rep.add_markdown("![alt text](images/portada-dgreport.png 'Portada')")
    rep.write_report()
