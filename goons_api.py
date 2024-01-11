import requests
from datetime import datetime
from pytz import timezone
from scrape_goon import scrape_goons, time_delta

class Goonies():
    def __init__(self):
        self.mapa_atual = None
        self.data_atual = None
        self.horario_atual = None
        self.report_id = None
        self.double_check_mark = None

    def request_goons_info(self):
        """
        Obtém as últimas informações sobre os Goons na API do TarkovPal
        Returna a última localização da seguinte forma: ReportID, Mapa Atual, Data Atual, Horário Atual
        """

        tarkovpal_api = 'https://tarkovpal.com/api'

        datetime_fmt = "%B %d, %Y, %I:%M %p"

        try:
            conteudo = requests.get(tarkovpal_api)
            goons_api = conteudo.json()

        except requests.exceptions.RequestException as e:
            print(e)                      
            # Envia notificação para o celular através do app NTFY informando erro
            requests.post('https://ntfy.sh/goonies-tarkovbr', data=f'API error: {e}'.encode(encoding='utf-8'))

        else:
            report_id = int(goons_api['Report'][0])
            mapa_atual = goons_api['Current Map'][0]
            edt = timezone('US/Eastern')
            gmt_brasil = timezone('America/Sao_Paulo')
            # define timezones
            data_hora_edt = edt.localize(datetime.strptime(goons_api['Time'][0], datetime_fmt))
            data_hora_brasil = data_hora_edt.astimezone(gmt_brasil)
            # converte horário EDT para GMT-3
            data_atual = data_hora_brasil.strftime('%d/%m/%Y')            
            horario_atual = data_hora_brasil.strftime('%H:%M %p')
            
            return report_id, mapa_atual, data_atual, horario_atual, data_hora_brasil

    def update_goons_info(self):
        """
        Verifica o #id do último report e atualiza as infos dos goons caso o #id aponte novo report
        """
        try:
            atualiza_localizacao_goons = self.request_goons_info()
                
        except requests.exceptions.RequestsException as e:
            requests.post('https://ntfy.sh/goonies-tarkovbr', data=f'Atualização localização error: {e}'.encode(encoding='utf-8'))
            
        else:
            if atualiza_localizacao_goons is not None:
                tp_report_id, tp_mapa, tp_data, tp_hora, tp_data_hora = atualiza_localizacao_goons

            # unpack de dados raspados do goon tracker
            gt_mapa, _, _, gt_data_hora = scrape_goons()            
            
            # verifica o último report id do tarkovpal e compara com o report id já armazenado
            if self.report_id == None or tp_report_id > self.report_id:
                # caso o intervalo de tempo entre os reports seja menor que 30 minutos, atualiza as infos com double check
                # caso contrário retorna single check e assume valor do tarkovpal para publicação no discord
                intervalo_de_tempo = time_delta(tp_data_hora, gt_data_hora)
                if tp_mapa == gt_mapa and intervalo_de_tempo < 90:
                    self.mapa_atual = tp_mapa
                    self.data_atual = tp_data
                    self.horario_atual = tp_hora
                    self.report_id = tp_report_id
                    self.double_check_mark = True
                else:
                    self.mapa_atual = tp_mapa
                    self.data_atual = tp_data
                    self.horario_atual = tp_hora
                    self.report_id = tp_report_id
                    self.double_check_mark = False
        
        return self.report_id, self.mapa_atual, self.data_atual, self.horario_atual, self.double_check_mark
                