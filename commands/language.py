from discord.ext import commands
from modules.i18n import LOCALES, t


@commands.command(usage="language.usage")
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def language(ctx, lang: str | None = None):
    "language.help"
    if not lang:
        return await ctx.send(t("language.current", ctx.language))
    lang = lang.lower()
    if lang not in LOCALES:
        return await ctx.send(
            t(
                "language.unavailable",
                ctx.language,
                languages=", ".join(LOCALES),
            )
        )
    await ctx.bot.guilds_data.upsert(
        guild_id=str(ctx.guild.id),
        language=lang,
    )
    await ctx.bot.get_language.delete(ctx.guild)
    await ctx.send(t("language.switched", lang))


async def setup(bot):
    bot.add_command(language)
