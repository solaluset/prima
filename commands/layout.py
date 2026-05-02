import discord
from discord.ext import commands
from discord.app_commands import context_menu, locale_str

from modules import embed
from modules.i18n import t

ENG = "`qwertyuiop[]\\asdfghjkl;'zxcvbnm,./@#$^&QWERTYUIOP{}|ASDFGHJKL:\"ZXCVBNM<>?"
UKR = "'йцукенгшщзхїґфівапролджєячсмитьбю.\"№;:?ЙЦУКЕНГШЩЗХЇҐФІВАПРОЛДЖЄЯЧСМИТЬБЮ,"
TR = str.maketrans(UKR + ENG, ENG + UKR)


async def _text_from_message(message: discord.Message | discord.MessageSnapshot) -> str:
    if message.content or isinstance(message, discord.MessageSnapshot):
        return message.content

    return await _text_from_referenced_message(message)


async def _text_from_referenced_message(message: discord.Message) -> str:
    if message.message_snapshots:
        return await _text_from_message(message.message_snapshots[0])

    if ref := message.reference:
        try:
            return (
                ref.cached_message or await message.channel.fetch_message(ref.message_id)
            ).content
        except discord.Forbidden:
            return ""

    return ""


@commands.command(usage="layout.usage", aliases=("lo",))
async def layout(ctx, *, text: str | None = None):
    "layout.help"
    if not text:
        try:
            text = await _text_from_referenced_message(ctx.message)
        except discord.NotFound:
            return await ctx.send(t("errors.not_found.message", ctx.language))
    if not text:
        return await ctx.send(t("layout.missing_text", ctx.language))
    em = embed.Embed(
        ctx,
        title=t("layout.title", ctx.language),
        description=text.translate(TR),
    )
    await em.send()


@context_menu(
    name=locale_str("layout.title"),
)
async def layout_message(ctx, message: discord.Message):
    language = await ctx.client.get_language(ctx.guild)
    try:
        text = await _text_from_message(message)
    except discord.NotFound:
        return await ctx.respond(t("errors.not_found.message", language), ephemeral=True)
    if not text:
        return await ctx.respond(t("layout.missing_text", language), ephemeral=True)
    em = discord.Embed(
        title=t("layout.title", language),
        description=text.translate(TR),
    )
    await ctx.response.send_message(embed=em, ephemeral=True)


async def setup(bot):
    bot.add_command(layout)
    bot.tree.add_command(layout_message)
