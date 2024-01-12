import discord
from discord import Embed
from discord.ext import tasks
from bot_info import botsecret
from goons_api import Goonies
from scrape_goon import configuracao_mapa

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.report_id_atual = None
        self.mapa_atual = None
        self.horario_atual = None
        self.data_atual = None
        self.check_mark = None

    async def setup_hook(self) -> None:
        # Roda a task no background
        self.my_background_task.start()

    async def on_ready(self):
        print(f'Logado como {self.user} (ID: {self.user.id})')
        print('------')

    # Mentioning
    # User <@USER_ID>
    # Role <@&ROLE_ID>
    # Channel <#CHANNEL_ID>
    # Emoji <:EMOJI_NAME:EMOJI_ID> <:mmLol:216154654256398347> // <a:nyancat:392938283556143104>

    @tasks.loop(seconds=600)  # Task é executada a cada 10 minutos
    async def my_background_task(self):
        channel = self.get_channel(1161828992102432808)  # ID do canal onde a msg será enviada ID do canal: 1161828992102432808
        goonies = Goonies()
        novo_report_id, self.mapa_atual, self.data_atual, self.horario_atual, self.check_mark = goonies.update_goons_info()

        if self.report_id_atual == None or self.report_id_atual < novo_report_id:
            self.report_id_atual = novo_report_id

            imagem_raid_atual, cor_raid_thumb, icon_url_check_mark = configuracao_mapa(self.mapa_atual, self.check_mark)            
            alerta_exclusivo = '<:goons_tracker:1185796465260515419><@&1185288986281914409> alerta exclusivo pra Nitro Boosters e VIPs'
            embed_goons = Embed(title='Goons Tracker', color=cor_raid_thumb)
            embed_goons.set_image(url=imagem_raid_atual)
            embed_goons.set_thumbnail(url=icon_url_check_mark)
            embed_goons.add_field(name='Raid', value=self.mapa_atual, inline=False)
            embed_goons.add_field(name='Data', value=self.data_atual, inline=True)
            embed_goons.add_field(name='Horário', value=f'{self.horario_atual} (horário de Brasília)', inline=True)            
            # embed_goons.add_field(name='Alerta', value='<@&1185288986281914409> alerta exclusivo pra Nitro Boosters e VIPs', inline=False)
            embed_goons.set_footer(text='Goonies: Goons Tracker do Tarkov Brasil', icon_url='https://cdn.discordapp.com/attachments/1166543939898195979/1166544051219210260/EFT-BR_LOGO_2.png?ex=6594b3cf&is=65823ecf&hm=cdecede7f33b0164c5f56e659f8600e5745d7cec9b80cabad7020cbeec467b6f&')
            print(f'{self.mapa_atual} - {self.data_atual} - {self.horario_atual} - {self.check_mark}')
            
            # envia a mensagem no canal com o mapa atual dos goons
            await channel.send(alerta_exclusivo, allowed_mentions=discord.AllowedMentions(roles=True))
            await channel.send(embed=embed_goons)       
        
    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # aguarda o bot estar pronto para rodar a task

client = MyClient(intents=discord.Intents.default())
client.run(botsecret)
    