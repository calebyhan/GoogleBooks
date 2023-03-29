from typing import Optional

import discord
from discord import ui
from discord.ext import commands, menus
from discord.ext.menus import button, First, Last

import json
import requests
from decouple import config

TOKEN = config("TOKEN")

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

bot = Bot()

class MySource(menus.ListPageSource):
    async def format_page(self, menu, entries):
        embed = discord.Embed(
            description=f"This is number {entries}.", 
            color=discord.Colour.random()
        )
        embed.set_footer(text=f"Requested by {menu.ctx.author}")
        return embed

class MyMenuPages(ui.View, menus.MenuPages):
    def __init__(self, source):
        super().__init__(timeout=60)
        self._source = source
        self.current_page = 0
        self.ctx = None
        self.message = None

    async def start(self, ctx, *, channel=None, wait=False):
        await self._source._prepare_once()
        self.ctx = ctx
        self.message = await self.send_initial_message(ctx, ctx.channel)

    async def _get_kwargs_from_page(self, page):
        value = await super()._get_kwargs_from_page(page)
        if 'view' not in value:
            value.update({'view': self})
        return value

    async def interaction_check(self, interaction):
        return interaction.user == self.ctx.author

    @ui.button(emoji='◀️', style=discord.ButtonStyle.blurple)
    async def before_page(self, button, interaction):
        await self.show_checked_page(self.current_page - 1)

    @ui.button(emoji='⏹️', style=discord.ButtonStyle.blurple)
    async def stop_page(self, button, interaction):
        self.stop()

    @ui.button(emoji='▶️', style=discord.ButtonStyle.blurple)
    async def next_page(self, button, interaction):
        await self.show_checked_page(self.current_page + 1)


@bot.command()
async def test(ctx):
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    formatter = MySource(data, per_page=1)
    menu = MyMenuPages(formatter)
    await menu.start(ctx)


bot.run(TOKEN)
