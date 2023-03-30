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

    selection = interactions.SelectMenu(
        options=[
            interactions.SelectOption(label="Main", value="main"),
            interactions.SelectOption(label="Subjects", value="subjects"),
            interactions.SelectOption(label="People", value="people"),
            interactions.SelectOption(label="More info", value="info")
        ],
        placeholder="Choose your option",
        custom_id="menu_select",
        min_values=1,
        max_values=1,
        )
    
    menu = "main"

    if choice == "title":
        book = requests.get(URL + response["docs"][0]["key"] + ".json").json()

        authors = []
        for i in book["authors"]:
            author = requests.get(URL + i["author"]["key"] + ".json").json()
            authors.append(author["name"])
        
        if menu == "main":
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
            ).set_footer("https://openlibrary.org").set_image(url="https://covers.openlibrary.org/b/id/" + str(book["covers"][0]) + "-L.jpg")
        elif menu == "subjects":
            embed = interactions.Embed(
                title="Search results",
                fields=[
                    interactions.EmbedField(
                        name=book["Subjects"],
                        value=", ".join(book["subjects"])
                    )
                ],
                timestamp=datetime.datetime.utcnow()
            ).set_footer("https://openlibrary.org")
        elif menu == "people":
            embed = interactions.Embed(
                title="Search results",
                fields=[
                    interactions.EmbedField(
                        name=book["Subjects"],
                        value=", ".join(book["subject_people"])
                    )
                ],
                timestamp=datetime.datetime.utcnow()
            ).set_footer("https://openlibrary.org")
        else:
            embed = interactions.Embed(
                title="Search results",
                fields=[
                    interactions.EmbedField(
                        name="More info",
                        value=f"""ISBN : {book['key'].split("/")[-1]}
                        Book link: https://openlibrary.org{book['key']}
                        Website revisions: {str(book["revision"])}
                        """
                    )
                ],
                timestamp=datetime.datetime.utcnow()
            ).set_footer("https://openlibrary.org")
        await ctx.send(embeds=embed, components=selection)
    ctx, menu = await bot.wait_for_select("menu_select")
    print(menu)

bot.start()