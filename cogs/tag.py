import discord
from discord.ext import commands
import json
import os
from utils.paginators import PaginatorsView
class Tag(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file = "tag.json"

    @commands.group(name="tag", invoke_without_command=True)
    async def tag(self, ctx, name: str = None):
            '''if name is None:
                your group code here'''
            #else:
            guild_id = str(ctx.guild.id)

            if os.path.exists(self.file):
                with open(self.file, "r") as f:
                    data = json.load(f)
            else:
                data = {}

            if guild_id in data and name in data[guild_id]["tags"]:
                tag_content = data[guild_id]["tags"][name]
                await ctx.send(tag_content)
            else:
                await ctx.send(f"Tag `{name}` not found.")


    @tag.command(name="create")
    async def create(self, ctx, name: str, *, content: str):
        guild_id = str(ctx.guild.id)

        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                data = json.load(f)
        else:
            data = {}

        if guild_id not in data:
            data[guild_id] = {"tags": {}}

        if name in data[guild_id]["tags"]:
            await ctx.send(f"Tag `{name}` already exists with content: {data[guild_id]['tags'][name]}")
            return

        data[guild_id]["tags"][name] = content

        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"Tag `{name}` created successfully!")

    @tag.command(name="delete")
    async def delete(self, ctx, name: str):
        guild_id = str(ctx.guild.id)

        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                data = json.load(f)
        else:
            data = {}

        if guild_id not in data or name not in data[guild_id]["tags"]:
            await ctx.send(f"Tag `{name}` not found.")
            return

        del data[guild_id]["tags"][name]

        if not data[guild_id]["tags"]:
            del data[guild_id]

        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"Tag `{name}` deleted successfully!")

    @tag.command(name="fetch")
    async def fetch(self, ctx, name: str):
        guild_id = str(ctx.guild.id)

        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                data = json.load(f)
        else:
            data = {}

        if guild_id in data and name in data[guild_id]["tags"]:
            tag_content = data[guild_id]["tags"][name]
            await ctx.send(tag_content)
        else:
            await ctx.send(f"Tag `{name}` not found.")
    @tag.command(name="config")
    async def config(self, ctx):
        guild_id = str(ctx.guild.id)

        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                data = json.load(f)
        else:
            data = {}

        if guild_id not in data or not data[guild_id]["tags"]:
            await ctx.send("No tags found for this guild.")
            return

        em_list = []
        tags = data[guild_id]["tags"]
        tag_list = "\n".join(
            f"Tag - **{tag}**\nContent - **{content}**\n"
            for tag, content in tags.items()
            )

        listem =discord.Embed(color=discord.Color.green)
        listem.title = "Tag Configuration"
        listem.description = "".join(tag_list)
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        em_list.append(listem)
        page = PaginatorsView(embed_list=em_list,ctx=ctx)
        await page.start(ctx)

def setup(bot):
    bot.add_cog(Tag(bot))
