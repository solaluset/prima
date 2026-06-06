import discord
from discord.app_commands import context_menu, locale_str

from modules.i18n import t


@context_menu(
    name=locale_str("..."),
)
async def get_edit_time(ctx, message: discord.Message):
    language = await ctx.client.get_language(ctx.guild)
    await ctx.response.send_message(t("#", language), ephemeral=True)


async def setup(bot):
    bot.tree.add_command(get_edit_time)
