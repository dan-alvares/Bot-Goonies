import discord
from discord import Embed
from discord.ext import tasks
from bot_info import botsecret
from scrape_goon import scrape_goons_raid

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.raid_atual = None
        self.horario_atual = None
        self.data_atual = None

    async def setup_hook(self) -> None:
        # Roda a task no background
        self.my_background_task.start()

    async def on_ready(self):
        print(f'Logado como {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(seconds=300)  # Task é executada a cada 5 minutos
    async def my_background_task(self):
        channel = self.get_channel(1161828992102432808)  # ID do canal onde a msg será enviada ID do canal: 1161828992102432808
        obtem_info_goons = scrape_goons_raid()
        if self.raid_atual != obtem_info_goons[0] or self.horario_atual != obtem_info_goons[2]:
            self.raid_atual = obtem_info_goons[0]
            self.data_atual = obtem_info_goons[1]
            self.horario_atual = obtem_info_goons[2]            

            if self.raid_atual == 'Customs':
                imagem_thumb = 'https://cdn.discordapp.com/attachments/1166543939898195979/1171767722191884308/customs2.jpg?ex=655de0bb&is=654b6bbb&hm=a677579f5a69b7e7194438b545562c93f9e7693b5067c9c84d5dc717705e3cbe&'
                cor_thumb = 15548997
            elif self.raid_atual == 'Lighthouse':
                imagem_thumb = 'https://cdn.discordapp.com/attachments/1166543939898195979/1171767722468704396/lighthouse2.jpg?ex=655de0bb&is=654b6bbb&hm=345e24245b756ba2b76cf610e3f960f096e61def238907ad8bab1ce75abb0396&'
                cor_thumb = 16776960
            elif self.raid_atual == 'Woods':
                imagem_thumb = 'https://cdn.discordapp.com/attachments/1166543939898195979/1171767721898278982/woods2.jpg?ex=655de0bb&is=654b6bbb&hm=65e2c9ee37120976c68e116f98feb830abcdec71fa30669a21a832372c4cfb89&'
                cor_thumb = 5763719
            elif self.raid_atual == 'Shoreline':
                imagem_thumb = 'https://cdn.discordapp.com/attachments/1166543939898195979/1171767722716172371/shoreline2.jpg?ex=655de0bb&is=654b6bbb&hm=bb29c3759070e218ee59168916956a7410661cc369922dee581e4ec0ea7fb539&'
                cor_thumb = 1752220

            embed_goons = Embed(title='Goons Tracker', color=cor_thumb)
            embed_goons.set_image(url=imagem_thumb)
            embed_goons.add_field(name='Raid', value=self.raid_atual, inline=False)
            embed_goons.add_field(name='Data', value=self.data_atual, inline=True)
            embed_goons.add_field(name='Horário', value=f'{self.horario_atual} (horário de Brasília)', inline=True)            
            embed_goons.set_footer(text='Escape from Tarkov Brasil', icon_url='https://cdn.discordapp.com/attachments/1166543939898195979/1166544051219210260/EFT-BR_LOGO_2.png?ex=65541a4f&is=6541a54f&hm=8dd4f02d722b563a0aea69608e4182ac56907c7cc709e19eba3eb871e80dc532&')
            print(f'{self.raid_atual} - {self.data_atual} - {self.horario_atual}')
            
            await channel.send(embed=embed_goons) # envia a mensagem no canal com o mapa atual dos goons      
        
    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # aguarda o bot estar pronto para rodar a task

client = MyClient(intents=discord.Intents.default())
client.run(botsecret)
    