import discord
from discord.ext import commands
import re
import requests


class Yoink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def yoink(self, ctx, message):
        try:
            # check if bot has permissions
            if not ctx.guild.me.guild_permissions.manage_emojis:
                return await ctx.send("I don't have permission to add emotes to this server.")

            # check if user has permissions
            if not ctx.author.guild_permissions.manage_emojis:
                return await ctx.send("You don't have permission to add emotes to this server.")

            emoteregex = re.compile(r"https:\/\/7tv.app\/emotes\/(\w+)")

            # if doesnt match regex
            if not emoteregex.match(message):
                return await ctx.send("That's not a 7TV emote.")

            emoteid = emoteregex.sub(r"\1", message)

            emote = requests.get(
                f"https://7tv.io/v3/emotes/{emoteid}").json()
            emotename = emote["name"]
            emoteurl = f"https://cdn.7tv.app/emote/{emoteid}/2x.{'gif' if emote['animated'] else 'png'}"

            # get server emotes and check if emote already exists
            emotes = await ctx.guild.fetch_emojis()
            for emote in emotes:
                if emote.name == emotename:
                    return await ctx.send("That emote already exists in this server.")


            # download emote
            emote = requests.get(emoteurl)

            try:
                # add emote to server
                emote = await ctx.guild.create_custom_emoji(name=emotename, image=emote.content)
                await ctx.send(f"Added `{emotename}` to the server! {emote}")
            except:
                await ctx.send(f"There is either no slots available on server or I don't have permissions to add new emotes!")
                return

            # delete the message
            await ctx.message.delete()
        except Exception as e:
            await ctx.send(f"Error while handling request: {e}")
            return


async def setup(bot):
    await bot.add_cog(Yoink(bot))
