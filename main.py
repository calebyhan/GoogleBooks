from typing import Optional

import discord
from discord import ui
from discord.ext import commands, menus
from discord.ext.menus import button, First, Last

import os
import json
import requests

import discord


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


bot.run('MTA4NzU2NzM1NDE0MzE5NTIyOA.Gc_MYR.zpr1-SAmtK_-vemx_cOFrGOHrbClNG2YjOKo8M')

# from typing import Optional

# import discord
# from discord import app_commands
# from discord.ext import menus
# from discord.ext.menus import button, First, Last

# import os
# import json
# import requests


# MY_GUILD = discord.Object(id=905301278647783424)
# TOKEN = os.environ['api_key']
# URL = "https://openlibrary.org/"

# class MyClient(discord.Client):
#   def __init__(self, *, intents: discord.Intents):
#     super().__init__(intents=intents)
#     self.tree = app_commands.CommandTree(self)

#   async def setup_hook(self):
#     self.tree.copy_global_to(guild=MY_GUILD)
#     await self.tree.sync(guild=MY_GUILD)

# class MyMenuPages(menus.MenuPages, inherit_buttons=False):
#     @button('<:before_check:754948796487565332>', position=First(1))
#     async def go_to_previous_page(self, payload):
#         await self.show_checked_page(self.current_page - 1)

#     @button('<:next_check:754948796361736213>', position=Last(1))
#     async def go_to_next_page(self, payload):
#         await self.show_checked_page(self.current_page + 1)

#     @button('<:stop_check:754948796365930517>', position=Last(0))
#     async def stop_pages(self, payload):
#         self.stop()

# class MySource(menus.ListPageSource):
#     async def format_page(self, menu, entries):
#         embed = discord.Embed(
#             description=f"This is number {entries}.", 
#             color=discord.Colour.random()
#         )
#         embed.set_footer(text=f"Requested by {menu.ctx.author}")
#         return embed


# intents = discord.Intents.default()
# client = MyClient(intents=intents)


# @client.event
# async def on_ready():
#   print(f'Logged in as {client.user} (ID: {client.user.id})')
#   print('------')


# @client.tree.command()
# @app_commands.describe(
#   query="Look up:",
# )
# # @app_commands.choices(choices=[
# #   app_commands.Choice(name="q", value="q"),
# #   app_commands.Choice(name="title", value="title"),
# #   app_commands.Choice(name="author", value="author"),
# # ])
# async def search(interaction: discord.Interaction, query: str):
#   response = requests.get(URL + "search.json?q=" + query.replace(" ", "+")).json()
#   print(type)
#   data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#   formatter = MySource(data, per_page=1)
#   menu = MyMenuPages(formatter)
#   await menu.start(ctx)
  # await interaction.response.send_message(f'asds')
  


# client.run(TOKEN)
# @client.tree.command()
# @app_commands.rename(text_to_send='text')
# @app_commands.describe(text_to_send='Text to send in the current channel')
# async def send(interaction: discord.Interaction, text_to_send: str):
#     """Sends the text into the current channel."""
#     await interaction.response.send_message(text_to_send)


# @client.tree.command()
# @app_commands.describe(member='The member you want to get the joined date from; defaults to the user who uses the command')
# async def joined(interaction: discord.Interaction, member: Optional[discord.Member] = None):
#     """Says when a member joined."""
#     member = member or interaction.user

#     await interaction.response.send_message(f'{member} joined {discord.utils.format_dt(member.joined_at)}')


# @client.tree.context_menu(name='Show Join Date')
# async def show_join_date(interaction: discord.Interaction, member: discord.Member):
#     await interaction.response.send_message(f'{member} joined at {discord.utils.format_dt(member.joined_at)}')

# embed example

# @client.tree.context_menu(name='Report to Moderators')
# async def report_message(interaction: discord.Interaction, message: discord.Message):
#     await interaction.response.send_message(
#         f'Thanks for reporting this message by {message.author.mention} to our moderators.', ephemeral=True
#     )

#     log_channel = interaction.guild.get_channel(0)  # replace with your channel id

#     embed = discord.Embed(title='Reported Message')
#     if message.content:
#         embed.description = message.content

#     embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
#     embed.timestamp = message.created_at

#     url_view = discord.ui.View()
#     url_view.add_item(discord.ui.Button(label='Go to Message', style=discord.ButtonStyle.url, url=message.jump_url))

#     await log_channel.send(embed=embed, view=url_view)

# import discord
# from discord.ext import commands
# import commands
# import requests
# import json
# import os
# import keep_alive

# MY_GUILD = discord.Object(id=905301278647783424)
# TOKEN = os.environ['api_key']
# URL = "https://openlibrary.org/"

# class Bot(discord.ext.commands.Bot):
#     async def on_ready(self):
#         await self.tree.sync(guild=MY_GUILD)

# bot: commands.Bot = Bot

# @bot.tree.command(guild=MY_GUILD)
# async def slash(interaction: discord.Interaction, number: int, string: str):
#     await interaction.response.send_message(f'Modify {number=} {string=}', ephemeral=True)

# bot.tree.add_command(commands.Commands(bot), guild=MY_GUILD)

# if __name__ == "__main__":
#     bot.run(TOKEN)


# @bot.add_command()
# async def searchbook(ctx, book):
#   response = requests.get(url + "search.json", params={"q": book}).json()
#   with open("embeds.json", "r") as f:
#     reply = json.load(f)
#     embed = discord.Embed(
#         title='Page 1',
#         description='This is the first page of the embed.'
#     )

#     embed.add_field(
#         name='Page 2',
#         value='This is the second page of the embed.'
#     )

#     embed.add_field(
#         name='Page 3',
#         value='This is the third page of the embed.'
#     )

#     msg = await ctx.send(embed=embed)

#     await msg.add_reaction('⬅️')
#     await msg.add_reaction('➡️')

# @bot.event
# async def on_reaction_add(reaction, user):
#     if user.bot or not reaction.message.author == bot.user:
#         return

#     if reaction.emoji in ['⬅️', '➡️']:
#         embed = reaction.message.embeds[0]

#         current_page = int(embed.title.split()[-1])

#         total_pages = len(embed.fields)

#         if reaction.emoji == '⬅️':
#             new_page = current_page - 1 if current_page > 1 else total_pages
#         elif reaction.emoji == '➡️':
#             new_page = current_page + 1 if current_page < total_pages else 1

#         embed.set_field_at(0, name=f'Page {new_page}', value=embed.fields[new_page-1].value)
#         embed.title = f'Page {new_page}'

#         await reaction.message.edit(embed=embed)

# needs to be in command func
# while True:
#   button = await bot.wait_for("button_click", check = lambda i: i.custom_id in ["button1", "button3"])

#   if button.custom_id == "button1":
#       await button.send(content="Button clicked!", ephemeral=False)
#   else:
#       await button.send(content="Button smashed!", ephemeral=False)