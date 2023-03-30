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

    selection1 = interactions.SelectMenu(
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
    
    selection2 = interactions.SelectMenu(
        options=[
            interactions.SelectOption(label="Main", value="main"),
            interactions.SelectOption(label="Bio", value="bio"),
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
            try:
                description=book["description"]
            except:
                description="None"
            embed = interactions.Embed(
                title="Search results",
                fields=[
                    interactions.EmbedField(
                        name=book["title"],
                        value=", ".join(authors)
                    ),
                    interactions.EmbedField(
                        name="Description",
                        value=description
                    )
                ],
                timestamp=datetime.datetime.utcnow()
            ).set_footer("https://openlibrary.org").set_image(url="https://covers.openlibrary.org/b/id/" + str(book["covers"][0]) + "-L.jpg")
        elif menu == "subjects":
            try:
                subjects = book["subjects"]
            except:
                subjects = "None"
            embed = interactions.Embed(
                title="Search results",
                fields=[
                    interactions.EmbedField(
                        name=book["Subjects"],
                        value=", ".join(subjects)
                    )
                ],
                timestamp=datetime.datetime.utcnow()
            ).set_footer("https://openlibrary.org")
        elif menu == "people":
            try:
                people = book["subject_people"]
            except:
                people = "None"
            embed = interactions.Embed(
                title="Search results",
                fields=[
                    interactions.EmbedField(
                        name=book["Subjects"],
                        value=", ".join(people)
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
                        Book link: https://openlibrary.org/works/{book['key']}
                        Website revisions: {str(book["revision"])}
                        """
                    )
                ],
                timestamp=datetime.datetime.utcnow()
            ).set_footer("https://openlibrary.org")
        await ctx.send(embeds=embed, components=selection1)
    elif choice == "author":
        authorID = requests.get(URL + "search/authors.json?q=" + query.replace(" ", "+")).json()["docs"][0]["key"]
        author = requests.get(URL + "/authors/" + authorID + ".json").json()

        if menu == "main":
            try:
                deathdate = author["death_date"]
            except:
                deathdate = "Present"
            try:
                birthdate = author["birth_date"]
            except:
                birthdate = "Unknown"
                deathdate = "Unknown"
            embed = interactions.Embed(
                title="Search results",
                fields=[
                    interactions.EmbedField(
                        name=author["name"],
                        value=f"{birthdate} - {deathdate}"
                    )
                ],
                timestamp=datetime.datetime.utcnow()
            ).set_footer("https://openlibrary.org")
        elif menu == "bio":
            try:
                bio = author["bio"]
            except:
                bio = "None"
            embed = interactions.Embed(
                title="Search results",
                fields=[
                    interactions.EmbedField(
                        name="Biography",
                        value=bio
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
                        value=f"""ISBN : {authorID}
                        Author link: https://openlibrary.org/authors/{authorID}
                        Website revisions: {str(book["revision"])}
                        """
                    )
                ],
                timestamp=datetime.datetime.utcnow()
            ).set_footer("https://openlibrary.org")
        await ctx.send(embeds=embed, components=selection2)

    ctx, menu = await bot.wait_for_select("menu_select")
    print(menu)

bot.start()