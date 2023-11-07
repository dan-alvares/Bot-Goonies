import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
from pytz import timezone

link_tabela = 'https://docs.google.com/spreadsheets/u/0/d/e/2PACX-1vRwLysnh2Tf7h2yHBc_bpZLQh6DiFZtDqyhHLYP022xolQUPUHkSModV31E5Y7cLh_8LZGexpXy2VuH/pubhtml/sheet?headers=false&gid=1420050773' # tabela do google sheets com info 

def scrape_goons_raid():
    request_conteudo = requests.get(link_tabela) # dentro do loop do bot
    print(request_conteudo.status_code)

    soup = bs(request_conteudo.content, 'html.parser')
    tabela = soup.find_all('td') # pega todas as tags td da tabela

    mapa_atual = tabela[2].text # pega o mapa atual
    data_horario_goons = tabela[3].text # pega o horario dos goons

    formato_data_horario = '%m/%d/%Y %H:%M:%S'

    edt = timezone('US/Eastern')
    data_hora_edt = edt.localize(datetime.strptime(data_horario_goons, formato_data_horario))

    gmt_brasil = timezone('America/Sao_Paulo')
    data_hora_gmt_brasil = data_hora_edt.astimezone(gmt_brasil)
    data_hora_gmt_brasil.strftime('%d/%m/%Y %H:%M:%S') 
    data_atual = data_hora_gmt_brasil.strftime('%d/%m/%Y') 
    horario_atual = data_hora_gmt_brasil.strftime('%H:%M:%S') 
    return mapa_atual, data_atual, horario_atual
