import discord
from discord.app_commands import context_menu, locale_str

from modules.i18n import t


@context_menu(
    name=locale_str("etime.title"),
)
async def get_edit_time(inter, message: discord.Message):
    language = await inter.client.get_language(inter.guild)

    time = message.edited_at
    if time is None:
        await inter.response.send_message(
            t("etime.not-edited", language), ephemeral=True
        )
    else:
        await inter.response.send_message(
            t("etime.edited", language, time=f"<t:{int(time.timestamp())}:F>"),
            ephemeral=True,
        )


async def setup(bot):
    bot.tree.add_command(get_edit_time)
