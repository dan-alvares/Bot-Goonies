import discord
from discord import Embed, File
from discord.ext import tasks, commands
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
                imagem_thumb = 'https://media.discordapp.net/attachments/1166543939898195979/1171169676122927165/customs_thumb.jpg?ex=655bb3c2&is=65493ec2&hm=8f3dc555d25c5b5dc9cccd2b66cb24417cc6975806454bcdafbde5ee4e1061a6&='
                cor_thumb = 15548997
            elif self.raid_atual == 'Lighthouse':
                imagem_thumb = 'https://media.discordapp.net/attachments/1166543939898195979/1171169676445892608/lighthouse_thumb.jpg?ex=655bb3c2&is=65493ec2&hm=0e08f34f61960cd352a6c2f89eb923129c1e250f260c0192df32f124b7ec7aef&='
                cor_thumb = 16776960
            elif self.raid_atual == 'Woods':
                imagem_thumb = 'https://media.discordapp.net/attachments/1166543939898195979/1171169677012119604/woods_thumb.jpg?ex=655bb3c2&is=65493ec2&hm=c56eefd96f5479529d8948e9255db60577c6f6cff20329b10a088a5801416e0e&='
                cor_thumb = 5763719
            elif self.raid_atual == 'Shoreline':
                imagem_thumb = 'https://media.discordapp.net/attachments/1166543939898195979/1171169676726894622/shoreline_thumb.jpg?ex=655bb3c2&is=65493ec2&hm=573c8bc890044256da1ce4d311f1a640459ec0afdc6f786e1c12be8c9fcd48d3&='
                cor_thumb = 15105570

            embed_goons = Embed(title='Goons Tracker', color=cor_thumb)
            embed_goons.set_image(url=imagem_thumb)
            embed_goons.add_field(name='Raid', value=self.raid_atual, inline=False)
            embed_goons.add_field(name='Data', value=self.data_atual, inline=True)
            embed_goons.add_field(name='Horário', value=self.horario_atual, inline=True)            
            embed_goons.set_footer(text='Escape from Tarkov Brasil', icon_url='https://cdn.discordapp.com/attachments/1166543939898195979/1166544051219210260/EFT-BR_LOGO_2.png?ex=65541a4f&is=6541a54f&hm=8dd4f02d722b563a0aea69608e4182ac56907c7cc709e19eba3eb871e80dc532&')
            
            await channel.send(embed=embed_goons) # envia a mensagem no canal com o mapa atual dos goons      
        
    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # aguarda o bot estar pronto para rodar a task

client = MyClient(intents=discord.Intents.default())
client.run(botsecret)
    