import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
from pytz import timezone


def scrape_goons():
    link_tabela = 'https://docs.google.com/spreadsheets/u/0/d/e/2PACX-1vRwLysnh2Tf7h2yHBc_bpZLQh6DiFZtDqyhHLYP022xolQUPUHkSModV31E5Y7cLh_8LZGexpXy2VuH/pubhtml/sheet?headers=false&gid=1420050773' # tabela do google sheets com info 

    try:
        request_conteudo = requests.get(link_tabela)
        soup = bs(request_conteudo.content, 'html.parser')
        
        # pega todas as tags td da tabela
        tabela = soup.find_all('td') 

        # pega o mapa atual
        mapa_atual = tabela[2].text

        # pega o horario dos goons
        data_horario_goons = tabela[3].text 
        formato_data_horario = '%m/%d/%Y %H:%M:%S'

        # define timezones
        edt = timezone('US/Eastern')
        gmt_brasil = timezone('America/Sao_Paulo')

        # localiza timezone
        data_hora_edt = edt.localize(datetime.strptime(data_horario_goons, formato_data_horario))        

        # converte horário EDT para GMT-3
        data_hora_brasil = data_hora_edt.astimezone(gmt_brasil)

        # data_hora_gmt_brasil.strftime('%d/%m/%Y %H:%M:%S') 
        data_atual = data_hora_brasil.strftime('%d/%m/%Y') 
        horario_atual = data_hora_brasil.strftime('%H:%M %p')

    except requests.exceptions.RequestException as e:
        print(e)
        requests.post('https://ntfy.sh/goonies-tarkovbr', data=f'Scraping error: {e}'.encode(encoding='utf-8'))
        mapa_atual = None
        data_atual = None
        horario_atual = None
        data_hora_brasil = None
        return mapa_atual, data_atual, horario_atual, data_hora_brasil

    else:
        return mapa_atual, data_atual, horario_atual, data_hora_brasil

def time_delta(tempo_a, tempo_b):
    """
    Calcula o tempo decorrido entre dois horários em minutos, retornando valor inteiro
    """
    if tempo_a > tempo_b:
        tempo_delta = tempo_a - tempo_b
    else:
        tempo_delta = tempo_b - tempo_a
    tempo_delta = int(tempo_delta.total_seconds() / 60)

    return tempo_delta

def configuracao_mapa(mapa_atual, check_mark):
    """
    Retorna dados que irão configurar a embed enviada para o canal do Discord
    """
    # cores da barra da embed: https://gist.github.com/thomasbnt/b6f455e2c7d743b796917fa3c205f812
    mapas = {
        'Customs': {
            'imagem_thumb': 'https://cdn.discordapp.com/attachments/1166543939898195979/1171767722191884308/customs2.jpg?ex=655de0bb&is=654b6bbb&hm=a677579f5a69b7e7194438b545562c93f9e7693b5067c9c84d5dc717705e3cbe&',
            'cor_thumb': 15548997
        },
        'Lighthouse': {
            'imagem_thumb': 'https://cdn.discordapp.com/attachments/1166543939898195979/1171767722468704396/lighthouse2.jpg?ex=655de0bb&is=654b6bbb&hm=345e24245b756ba2b76cf610e3f960f096e61def238907ad8bab1ce75abb0396&',
            'cor_thumb': 16776960
        },
        'Woods': {
            'imagem_thumb': 'https://cdn.discordapp.com/attachments/1166543939898195979/1171767721898278982/woods2.jpg?ex=655de0bb&is=654b6bbb&hm=65e2c9ee37120976c68e116f98feb830abcdec71fa30669a21a832372c4cfb89&',
            'cor_thumb': 5763719
        },
        'Shoreline': {
            'imagem_thumb': 'https://cdn.discordapp.com/attachments/1166543939898195979/1171767722716172371/shoreline2.jpg?ex=655de0bb&is=654b6bbb&hm=bb29c3759070e218ee59168916956a7410661cc369922dee581e4ec0ea7fb539&',
            'cor_thumb': 3447003
        }
    }

    if mapa_atual in mapas:
        imagem_thumb = mapas[mapa_atual]['imagem_thumb']
        cor_thumb = mapas[mapa_atual]['cor_thumb']
    
    if check_mark == True:
        # retorna double check para construir a embed
        icon_url_check_mark = 'https://cdn.discordapp.com/attachments/1166543939898195979/1185313390332223569/double-check.png?ex=658f281e&is=657cb31e&hm=0d308e16130d164b1cf8c28c215bfbd829ef90d0e65480b8db955bfaf396c48b&'
    else:
        # retorno single check para construir a embed
        icon_url_check_mark = 'https://cdn.discordapp.com/attachments/1166543939898195979/1185313391120760922/single-check.png?ex=658f281e&is=657cb31e&hm=9d859227774b10f923a53ac7ce6f25530a7af02581fe1cef899a0c27edc9a485&'

    return imagem_thumb, cor_thumb, icon_url_check_mark
