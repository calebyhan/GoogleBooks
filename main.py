from typing import Optional

import interactions

import json
import requests
from decouple import config
import datetime
import random

URL = "https://openlibrary.org/"
TOKEN = config("TOKEN")

bot = interactions.Client(token=TOKEN, presence=interactions.ClientPresence(
        status=interactions.StatusType.IDLE,
        activities=[
            interactions.PresenceActivity(name="you vibing", type=interactions.PresenceActivityType.WATCHING)
        ]
    ))

print("Bot is on.")

@bot.command(name="search", description="Searches query", scope=905301278647783424)
@interactions.option("query")
@interactions.option(choices=[interactions.Choice(name="query", value="q"), interactions.Choice(name="title", value="title"), interactions.Choice(name="author", value="author")])
async def search_command(ctx: interactions.CommandContext, query: str, choice: str):
    await ctx.defer()
    response = requests.get(URL + "search.json?" + choice + "=" + query.replace(" ", "+")).json()
    book = requests.get(URL + response["docs"][0]["key"] + ".json").json()

    authors = []
    for i in book["authors"]:
        author = requests.get(URL + i["author"]["key"] + ".json").json()
        authors.append(author["name"])
    
    embed = interactions.Embed(
        title="Search results",
        fields=[
            interactions.EmbedField(
                name=book["title"],
                value=", ".join(authors)
            ),
            interactions.EmbedField(
                name="Description",
                value=book["description"]
            )
        ],
        timestamp=datetime.datetime.utcnow()
    ).set_footer("[https://openlibrary.org/](Open Library)")
    
    selection = interactions.SelectMenu(
        options=[
            interactions.SelectOption(label="Rock", emoji=interactions.Emoji(name="🪨"), value="rock"),
            interactions.SelectOption(label="Paper", emoji=interactions.Emoji(name="📃"), value="paper"),
            interactions.SelectOption(label="Scissors", emoji=interactions.Emoji(name="✂"), value="scissors"),
        ],
        placeholder="Choose your option",
        custom_id="rps_selection",
        min_values=1,
        max_values=1,
        )
    await ctx.send(embeds=embed, components=selection)

bot.start()